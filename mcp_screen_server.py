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
        self.save_dir = os.getenv('SCREEN_SAVE_DIR', "/Users/azhar/Desktop/others/claudeMCP/dump")
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
                    mimeType="image/webp",
                    description="Real-time screen capture in WebP format"
                )
            ]

        @self.app.read_resource()
        async def read_resource(uri: AnyUrl) -> str:
            try:
                if not str(uri).startswith("screen://") or not str(uri).endswith("/current"):
                    raise ValueError(f"Unknown resource: {uri}")
                
                screenshot = pyautogui.screenshot()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = os.path.join(self.save_dir, f"screen_capture_{timestamp}.webp")
                
                # Save the screenshot with dynamic compression to ensure it's under 500KB
                self.save_compressed_image(screenshot, filepath, target_size_kb=500)
                
                return json.dumps({
                    "timestamp": timestamp,
                    "path": filepath,
                    "size": {
                        "width": screenshot.width,
                        "height": screenshot.height
                    }
                }, indent=2)
            except Exception as e:
                self.logger.error(f"Error reading resource: {str(e)}", exc_info=True)
                raise ValueError("Failed to read resource.")

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
                    save_path = os.path.join(self.save_dir, f"screen_capture_{timestamp}.webp")
                else:
                    # Ensure the file has a .webp extension
                    if not save_path.lower().endswith('.webp'):
                        save_path += '.webp'
                
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                # Save the screenshot with dynamic compression
                self.save_compressed_image(screenshot, save_path, target_size_kb=500)
                
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
                self.logger.error(f"Screen capture error: {str(e)}", exc_info=True)
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({
                            "success": False,
                            "error": str(e)
                        }, indent=2)
                    )
                ]

    def save_compressed_image(self, image: Image.Image, filepath: str, target_size_kb: int = 500):
        """Save an image with dynamic compression to ensure it's under the target size."""
        # Define initial parameters for binary search
        min_quality = 20
        max_quality = 95
        target_size = target_size_kb * 1024  # Convert KB to Bytes
        quality = max_quality
        iteration = 0
        max_iterations = 7  # Limit iterations to prevent infinite loops

        while iteration < max_iterations:
            # Save image with current quality
            image.save(filepath, format='WEBP', quality=quality, method=6, optimize=True)
            size = os.path.getsize(filepath)
            
            self.logger.debug(f"Iteration {iteration}: quality={quality}, size={size / 1024:.2f}KB")
            
            if size <= target_size:
                self.logger.info(f"Image saved at quality={quality}, size={size / 1024:.2f}KB")
                return
            else:
                # Decrease quality for next iteration
                max_quality = quality - 1
                quality = (min_quality + quality) // 2  # Binary search approach
            
            iteration += 1

        # If target size not achieved, start resizing
        self.logger.warning(f"Could not achieve target size with quality >= {min_quality}. Resizing image.")
        new_width = int(image.width * 0.9)
        new_height = int(image.height * 0.9)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        self.save_compressed_image(resized_image, filepath, target_size_kb)

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