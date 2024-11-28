#!/usr/bin/env python3
import os
import json
import logging
from datetime import datetime
from collections.abc import Sequence
from typing import Any, Optional

import pyautogui
from PIL import Image
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl

class MCPScreenServer:
    def __init__(self):
        self.buffer = ""
        self.save_dir = "/Users/azhar/Desktop/others/claudeMCP/dump"
        os.makedirs(self.save_dir, exist_ok=True)
        self.app = Server("screen-server")
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("screen-server")
        
        # Set up server handlers
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.list_resources()
        async def list_resources() -> list[Resource]:
            uri = AnyUrl("screen://capture/current")
            return [
                Resource(
                    uri=uri,
                    name="Current screen capture",
                    mimeType="image/png",
                    description="Real-time screen capture"
                )
            ]

        @self.app.read_resource()
        async def read_resource(uri: AnyUrl) -> str:
            try:
                if not str(uri).startswith("screen://") or not str(uri).endswith("/current"):
                    raise ValueError(f"Unknown resource: {uri}")
                
                screenshot = pyautogui.screenshot()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = os.path.join(self.save_dir, f"screen_capture_{timestamp}.png")
                screenshot.save(filepath)
                
                return json.dumps({
                    "timestamp": timestamp,
                    "path": filepath,
                    "size": {
                        "width": screenshot.width,
                        "height": screenshot.height
                    }
                }, indent=2)
            except Exception as e:
                self.logger.error(f"Error reading resource: {str(e)}")
                raise

        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="capture_screen",
                    description="Capture current screen content",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "save_path": {
                                "type": "string",
                                "description": "Optional custom save path"
                            }
                        }
                    }
                )
            ]

        @self.app.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            if name != "capture_screen":
                raise ValueError(f"Unknown tool: {name}")

            try:
                screenshot = pyautogui.screenshot()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = arguments.get("save_path") if isinstance(arguments, dict) else None
                
                if not save_path:
                    save_path = os.path.join(self.save_dir, f"screen_capture_{timestamp}.png")
                
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                screenshot.save(save_path)
                
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "success": True,
                            "timestamp": timestamp,
                            "path": save_path,
                            "size": {
                                "width": screenshot.width,
                                "height": screenshot.height
                            }
                        }, indent=2)
                    )
                ]
            except Exception as e:
                self.logger.error(f"Screen capture error: {str(e)}")
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "success": False,
                            "error": str(e)
                        }, indent=2)
                    )
                ]

    async def run(self):
        """Main entry point for the server."""
        from mcp.server.stdio import stdio_server
        self.logger.info("Starting MCP Screen Server")
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )

async def main():
    server = MCPScreenServer()
    await server.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())