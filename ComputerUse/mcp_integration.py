import asyncio
import websockets
import json
import sys
import os

class MCPIntegration:
    def __init__(self):
        self.computer_uri = "ws://localhost:8767"  # Computer control server
        self.commands = [
            {"type": "keyboard", "action": "hotkey", "keys": ["command", "a"]},
            {"type": "keyboard", "action": "hotkey", "keys": ["command", "c"]},
            {"type": "system", "action": "get_mouse_position"},
            {"type": "mouse", "action": "move", "x": 500, "y": 500},
            {"type": "mouse", "action": "click"},
            {"type": "keyboard", "action": "hotkey", "keys": ["command", "v"]}
        ]

    async def execute_computer_commands(self):
        try:
            async with websockets.connect(self.computer_uri) as websocket:
                print("Connected to Computer Control Server")
                for cmd in commands:
                    print(f"\nExecuting: {json.dumps(cmd, indent=2)}")
                    await websocket.send(json.dumps(cmd))
                    response = await websocket.recv()
                    print(f"Response: {response}")
                    await asyncio.sleep(3)
        except Exception as e:
            print(f"Error with computer control: {e}")

async def main():
    mcp = MCPIntegration()
    await mcp.execute_computer_commands()

if __name__ == "__main__":
    # Use the python path from your config
    python_path = "/Users/azhar/Desktop/others/claudeMCP/mcp-server-py/.env/bin/python"
    if not os.path.exists(python_path):
        print(f"Warning: Python path {python_path} not found")
    
    asyncio.run(main())