#!/usr/bin/env python3
import os
import json
import logging
import duckdb
import threading
import time
import asyncio
from datetime import datetime
from collections.abc import Sequence
from typing import Any, Optional
from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# DuckDB cache management
duckdb_cache = {}
cache_access_times = {}

class QueryRequest(BaseModel):
    csv_file_path: str
    query: str

class MCPFastAPIServer:
    def __init__(self):
        self.app = Server("fastapi-mcp-server")
        self.fastapi_app = FastAPI()
        
        # Add CORS middleware
        self.fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("fastapi-mcp-server")
        
        # Set up handlers
        self.setup_handlers()
        self.setup_fastapi_routes()
        
        # Start cleanup thread
        self.cleanup_thread = threading.Thread(target=self.cleanup_duckdb_connections, daemon=True)
        self.cleanup_thread.start()

    def is_valid_csv_path(self, csv_file_path: str) -> bool:
        """Validate if the CSV path is safe to use"""
        csv_file_path = os.path.abspath(csv_file_path)
        return csv_file_path.endswith('.csv') and os.path.exists(csv_file_path)

    def get_cache_key(self, csv_path: str) -> str:
        """Generate cache key based on file path and modification time"""
        mod_time = os.path.getmtime(csv_path)
        return f"{csv_path}:{mod_time}"

    def load_csv_into_duckdb(self, csv_file_path: str) -> duckdb.DuckDBPyConnection:
        """Load CSV into DuckDB with caching"""
        if not self.is_valid_csv_path(csv_file_path):
            raise ValueError(f"Invalid or non-existent CSV file path: {csv_file_path}")

        cache_key = self.get_cache_key(csv_file_path)

        if cache_key in duckdb_cache:
            cache_access_times[cache_key] = time.time()
            return duckdb_cache[cache_key]
        else:
            conn = duckdb.connect(database=':memory:')
            conn.execute(f"CREATE TABLE data AS SELECT * FROM read_csv_auto('{csv_file_path}');")
            duckdb_cache[cache_key] = conn
            cache_access_times[cache_key] = time.time()
            return conn

    def cleanup_duckdb_connections(self):
        """Cleanup unused DuckDB connections periodically"""
        while True:
            time.sleep(3000)  # Check every 5 minutes
            current_time = time.time()
            to_delete = []
            for cache_key, last_access in cache_access_times.items():
                if current_time - last_access > 600:  # 10 minutes timeout
                    conn = duckdb_cache.get(cache_key)
                    if conn:
                        conn.close()
                    to_delete.append(cache_key)
            for cache_key in to_delete:
                del duckdb_cache[cache_key]
                del cache_access_times[cache_key]

    def setup_fastapi_routes(self):
        @self.fastapi_app.post("/execute_query")
        async def execute_query(request: QueryRequest):
            try:
                result = await self.execute_query_internal(
                    csv_file_path=request.csv_file_path,
                    query=request.query
                )
                return result
            except Exception as e:
                self.logger.error(f"Error processing request: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=str(e))

        @self.fastapi_app.get("/health")
        async def health_check():
            return {"status": "healthy", "server": "fastapi-mcp-server"}

    async def execute_query_internal(self, csv_file_path: str, query: str):
        """Execute DuckDB query on CSV data"""
        try:
            # Load CSV into DuckDB
            conn = self.load_csv_into_duckdb(csv_file_path)

            # Execute the query
            result = conn.execute(query).fetchall()
            columns = [desc[0] for desc in conn.description]
            
            # Process results
            processed_data = [dict(zip(columns, row)) for row in result]

            return {
                "success": True,
                "data": {
                    "columns": columns,
                    "rows": processed_data,
                    "rowCount": len(processed_data)
                }
            }

        except Exception as e:
            self.logger.error(f"Error executing query: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def setup_handlers(self):
        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="execute_query",
                    description="Execute DuckDB query on CSV file",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "csv_file_path": {
                                "type": "string",
                                "description": "Path to the CSV file"
                            },
                            "query": {
                                "type": "string",
                                "description": "DuckDB SQL query to execute"
                            }
                        },
                        "required": ["csv_file_path", "query"]
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            if name != "execute_query":
                raise ValueError(f"Unknown tool: {name}")

            try:
                result = await self.execute_query_internal(
                    csv_file_path=arguments.get("csv_file_path"),
                    query=arguments.get("query")
                )
                
                return [
                    TextContent(
                        type="text",
                        text=json.dumps(result, indent=2)
                    )
                ]

            except Exception as e:
                self.logger.error(f"Error processing request: {str(e)}", exc_info=True)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "success": False,
                            "error": str(e)
                        }, indent=2)
                    )
                ]

    async def run_fastapi(self):
        """Run the FastAPI server"""
        config = uvicorn.Config(
            self.fastapi_app, 
            host="0.0.0.0", 
            port=8010, 
            log_level="info",
            reload=False
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def run_mcp(self):
        """Run the MCP server"""
        from mcp.server.stdio import stdio_server
        self.logger.info("Starting MCP Server")
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )

    async def run(self):
        """Main entry point for the server"""
        self.logger.info("Starting FastAPI MCP Server")
        try:
            await asyncio.gather(
                self.run_fastapi(),
                self.run_mcp()
            )
        except Exception as e:
            self.logger.error(f"Server error: {str(e)}", exc_info=True)
            raise

async def main():
    try:
        server = MCPFastAPIServer()
        await server.run()
    except Exception as e:
        logging.error(f"Failed to start server: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server shutting down...")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
