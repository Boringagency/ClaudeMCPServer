# Claude MCP Server Collection

This repository contains a collection of Model Context Protocol (MCP) servers designed to enhance Claude's desktop application capabilities. Each server provides specific functionality that allows Claude to interact with your computer in different ways.

## Overview

The project consists of several MCP servers:
1. Screen Capture Server - Captures and processes screenshots
2. Computer Control Server - Enables keyboard and mouse automation
3. FastAPI Integration Server - Handles data processing and API endpoints
4. Curl Server - Provides HTTP request capabilities

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

### 1. Screen Capture Server

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

#### Testing:
```bash
python test_screen_server.py  # Run server tests
python test_capture.py        # Test basic capture functionality
```

### 2. Computer Control Server

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

#### Testing:
```bash
python ComputerUse/test_computer_control.py  # Test computer control features
python ComputerUse/test_client.py           # Test client connectivity
```

### 3. FastAPI Integration Server

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

#### API Endpoints:
- `/process` - Main data processing endpoint
  - Accepts POST requests with JSON data
  - Processes CSV files and returns analysis results

#### Testing FastAPI Server:
```bash
# Test the server directly
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"date_column":"Start Time","model_column":"Device Brand","csv_file_paths":"file1.csv,file2.csv"}'
```

### 4. Curl Server

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
    // ... other server configurations
  }
}
```

3. Configure GitHub integration (optional):
- Add your GitHub personal access token
- Update the GitHub username

### Starting All Services

1. Start the Screen Capture Server:
```bash
python mcp_screen_server.py
```

2. Start the Computer Control Server:
```bash
python ComputerUse/mcp_computer_server.py
```

3. Start the FastAPI Server:
```bash
python fastapi/main.py
```

4. Start the Integration Server:
```bash
python ComputerUse/full_mcp_integration.py
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
