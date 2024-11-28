#!/bin/bash

# Activate virtual environment if it exists
if [ -d "../.env" ]; then
    source ../.env/bin/activate
fi

# Make the Python script executable
chmod +x curl_mcp_server.py

# Run the server
python3 curl_mcp_server.py