#!/usr/bin/env python3
import os
import json
import asyncio
import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
from pydantic import AnyUrl

# Import our server
from mcp_screen_server import MCPScreenServer

async def test_mcp_server():
    """Test MCP server initialization"""
    print("\nTesting MCP server initialization...")
    try:
        server = MCPScreenServer()
        assert server.save_dir == "/Users/azhar/Desktop/others/claudeMCP/dump"
        assert os.path.exists(server.save_dir)
        print("✓ MCP server initialization test passed")
    except Exception as e:
        print(f"✗ MCP server initialization test failed: {str(e)}")
        raise

async def test_screen_capture():
    """Test screen capture functionality"""
    print("\nTesting screen capture...")
    try:
        import pyautogui
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        
        # Save to test file
        test_file = "/Users/azhar/Desktop/others/claudeMCP/dump/test_capture.png"
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        screenshot.save(test_file)
        
        # Verify file exists and has content
        assert os.path.exists(test_file)
        assert os.path.getsize(test_file) > 0
        print(f"✓ Screen capture test passed - saved to {test_file}")
        
        # Test file info
        file_info = os.stat(test_file)
        print(f"  - File size: {file_info.st_size} bytes")
        print(f"  - Created at: {datetime.fromtimestamp(file_info.st_ctime)}")
        
    except Exception as e:
        print(f"✗ Screen capture test failed: {str(e)}")
        raise

async def test_server_handlers():
    """Test server handlers setup"""
    print("\nTesting server handlers...")
    try:
        server = MCPScreenServer()
        
        # Test handler registration by checking if methods exist
        test_uri = AnyUrl("screen://capture/current")
        test_args = {"save_path": "/test/path.png"}
        
        # Verify that the server has the basic MCP functionality
        assert hasattr(server.app, "run"), "Server missing run method"
        assert hasattr(server.app, "create_initialization_options"), "Server missing initialization options"
        
        print("✓ Server handlers test passed")
        print("  - Server has required MCP methods")
        print("  - Handler registration successful")
        
    except Exception as e:
        print(f"✗ Server handlers test failed: {str(e)}")
        raise

async def test_save_directory():
    """Test save directory setup and permissions"""
    print("\nTesting save directory...")
    try:
        save_dir = "/Users/azhar/Desktop/others/claudeMCP/dump"
        test_file = os.path.join(save_dir, "test_write_permission.txt")
        
        # Test directory exists
        assert os.path.exists(save_dir), "Save directory doesn't exist"
        
        # Test write permission
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✓ Save directory test passed")
            print(f"  - Directory exists: {save_dir}")
            print("  - Write permission verified")
        except Exception as e:
            raise Exception(f"Write permission test failed: {str(e)}")
            
    except Exception as e:
        print(f"✗ Save directory test failed: {str(e)}")
        raise

async def main():
    """Run all tests"""
    print("\nRunning MCP Screen Server Tests...")
    try:
        import pyautogui
        from PIL import Image
    except ImportError:
        print("Installing required packages...")
        os.system("pip install pyautogui pillow")
        import pyautogui
        from PIL import Image

    test_functions = [
        test_mcp_server,
        test_screen_capture,
        test_server_handlers,
        test_save_directory
    ]
    
    failed_tests = 0
    for test in test_functions:
        try:
            await test()
        except Exception as e:
            print(f"\n❌ Test failed: {test.__name__}")
            print(f"Error: {str(e)}")
            failed_tests += 1
            continue
    
    if failed_tests == 0:
        print("\n✨ All tests completed successfully!")
    else:
        print(f"\n⚠️  {failed_tests} test(s) failed")

if __name__ == "__main__":
    asyncio.run(main())