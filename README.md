# Claude MCP Server Collection

This repository contains a collection of Model Context Protocol (MCP) servers designed to enhance Claude's desktop application capabilities. Each server provides specific functionality that allows Claude to interact with your computer in different ways.

## Latest Addition: DuckDB Integration! 🚀

New DuckDB FastAPI server for efficient large-scale data analysis:

### Example Queries and Results

#### Query 1: Analysis
![DuckDB Query Example 1](./fastapi/duckdb/assets/duckdb_query1.png)

#### Query 2: Aggregated Results
![DuckDB Query Example 2](./fastapi/duckdb/assets/duckdb_query2.png)

### DuckDB Server Features
- Analyze multiple CSV files (>1GB) directly in Claude Desktop
- Lightning-fast SQL queries with DuckDB
- Memory-efficient data processing
- Connection pooling and caching
- Automatic cleanup of unused connections

## Overview

The project consists of several MCP servers:
1. Screen Capture Server - Captures and processes screenshots
2. Computer Control Server - Enables keyboard and mouse automation
3. FastAPI Integration Server - Handles data processing and API endpoints
4. Curl Server - Provides HTTP request capabilities
5. DuckDB Server - Enables large-scale data analysis

## Prerequisites

- Python 3.8 or higher
- Node.js and npm (for filesystem server)
- Claude Desktop Application
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/syedazharmbnr1/ClaudeMCPServer.git
cd ClaudeMCPServer
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .env
source .env/bin/activate  # On Windows: .env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Server Components

### 1. DuckDB Server

Enables Claude to analyze large CSV files efficiently.

#### Setup and Usage:
```bash
cd fastapi/duckdb
python main.py
```

#### Features:
- Process multiple CSV files simultaneously
- Handle files larger than 1GB
- Fast SQL querying with DuckDB
- Memory-efficient processing
- Connection pooling

### 2. Screen Capture Server

Enables Claude to capture and process screenshots of your screen.

#### Setup and Usage:
```bash
python mcp_screen_server.py
```

#### Features:
- Real-time screen capture
- Dynamic image compression
- WebP format support for optimal file size
- Customizable save locations

### 3. Computer Control Server

Allows Claude to control mouse and keyboard actions.

#### Setup and Usage:
```bash
python ComputerUse/mcp_computer_server.py
```

#### Features:
- Mouse movement and clicks
- Keyboard shortcuts and text input
- Screen position tracking
- Clipboard operations

### 4. FastAPI Integration Server

The FastAPI server provides a robust API interface for data processing and integration.

#### Setup and Configuration:

1. Navigate to the FastAPI directory:
```bash
cd fastapi
```

2. Configure environment variables:
```bash
export PYTHONPATH=/path/to/mcp-server-py
export PORT=8000
```

3. Start the server:
```bash
python main.py
```

### 5. Curl Server

Provides HTTP request capabilities to Claude.

#### Setup:
```bash
cd Curl_Server
./start_server.sh  # For the basic server
./start_mcp_server.sh  # For the MCP integration
```

## Claude Desktop Integration

### Configuration

1. Copy the `claude_desktop_config.json` to your Claude Desktop app configuration directory

2. Update the paths in the configuration to match your system:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "<your-paths-here>"
      ]
    },
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
  }
}
```

## Testing

Each component has its own test suite:

```bash
# Test screen capture
python test_screen_server.py

# Test computer control
python ComputerUse/test_computer_control.py

# Test integration
python ComputerUse/test_client.py
```

## Troubleshooting

### Common Issues

1. Python Path Issues:
- Ensure PYTHONPATH is set correctly
- Verify virtual environment is activated

2. Permission Errors:
- Make sure script files are executable:
```bash
chmod +x *.py
chmod +x Curl_Server/*.sh
```

3. Port Conflicts:
- Screen Server: Default port 8767
- FastAPI Server: Default port 8000
- DuckDB Server: Default port 8010
- Integration Server: Default port 8768

### Logging

- Check `debug.log` for detailed error messages
- Each server component writes to its own log file

## Security Notes

1. GitHub Integration:
- Store your GitHub token securely
- Never commit tokens to the repository

2. File System Access:
- Configure filesystem paths carefully
- Limit access to necessary directories only

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
