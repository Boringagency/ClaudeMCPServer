# DuckDB FastAPI MCP Server

A FastAPI-based Model Context Protocol (MCP) server that provides DuckDB integration for efficient CSV file querying.

## Features

- FastAPI integration with MCP server
- DuckDB in-memory database for fast CSV querying
- Connection pooling and caching
- Automatic cleanup of unused connections
- CORS support
- Health check endpoint
- Error handling and logging

## Endpoints

- `POST /execute_query`: Execute DuckDB SQL queries on CSV files
- `GET /health`: Health check endpoint

## Configuration

The server runs on port 8010 by default and accepts the following environment variables:
- `PYTHONPATH`: Path to the MCP server root
- `PORT`: Server port (default: 8010)

## Usage

1. Start the server:
```bash
python main.py
```

2. Execute queries via the API:
```bash
curl -X POST http://localhost:8010/execute_query \
  -H "Content-Type: application/json" \
  -d '{
    "csv_file_path": "/path/to/your/file.csv",
    "query": "SELECT * FROM data LIMIT 5;"
  }'
```

## Features

- CSV file validation and path safety checks
- Connection caching for improved performance
- Automatic connection cleanup after 10 minutes of inactivity
- Error handling and detailed logging
- MCP tool integration for Claude AI

## Integration with Claude Desktop

Add the following configuration to your `claude_desktop_config.json`:

```json
"duckdb": {
  "command": "/path/to/python",
  "args": [
    "/path/to/fastapi/duckdb/main.py"
  ],
  "cwd": "/path/to/fastapi/duckdb",
  "env": {
    "PYTHONPATH": "/path/to/mcp-server-py",
    "PORT": "8010"
  }
}
```
