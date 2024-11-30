# DuckDB FastAPI MCP Server

A FastAPI-based Model Context Protocol (MCP) server that provides DuckDB integration for efficient CSV file querying and analysis, capable of handling large datasets (>1GB) directly through Claude Desktop.

## Example Queries and Results

### Query 1: Network Coverage Analysis
![DuckDB Query Example 1](./assets/duckdb_query1.png)

### Query 2: Aggregated Results
![DuckDB Query Example 2](./assets/duckdb_query2.png)

## Features

- FastAPI integration with MCP server
- DuckDB in-memory database for fast CSV querying of large files (>1GB)
- Efficient analysis of multiple CSV files simultaneously
- Connection pooling and caching
- Automatic cleanup of unused connections
- CORS support
- Health check endpoint
- Error handling and logging

## Query Examples

```sql
-- Example of analyzing multiple large CSV files
WITH coverage_summary AS (
  SELECT
    ROUND(Latitude, 2) as lat_round,
    ROUND(Longitude, 2) as lon_round,
    AVG("RSRP(ALL MRs) (dBm)") as avg_rsrp,
    SUM("UMR Count") as total_mr_count
  FROM data
  GROUP BY lat_round, lon_round
)
SELECT *
FROM coverage_summary
WHERE avg_rsrp < -90
ORDER BY total_mr_count DESC
LIMIT 10;
```

## Endpoints

- `POST /execute_query`: Execute DuckDB SQL queries on CSV files
- `GET /health`: Health check endpoint

## Large File Handling

DuckDB efficiently handles large CSV files by:
- Using memory-mapped files for data access
- Implementing parallel processing
- Providing optimized SQL execution
- Supporting streaming for large result sets

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
    "csv_file_path": "/path/to/your/large_file.csv",
    "query": "SELECT * FROM data LIMIT 5;"
  }'
```

## Features

- CSV file validation and path safety checks
- Connection caching for improved performance
- Automatic connection cleanup after 10 minutes of inactivity
- Error handling and detailed logging
- MCP tool integration for Claude AI
- Support for large file analysis (>1GB)
- Multi-file query capabilities

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