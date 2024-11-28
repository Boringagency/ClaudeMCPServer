import asyncio
import websockets
import json

async def execute_mcp_commands():
    uri = "ws://localhost:8767"
    commands = [
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "a"]},
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "c"]},
        {"type": "system", "action": "get_mouse_position"},
        {"type": "mouse", "action": "move", "x": 500, "y": 500},
        {"type": "mouse", "action": "click"},
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "v"]}
    ]
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to MCP server")
            for cmd in commands:
                print(f"\nExecuting command: {json.dumps(cmd, indent=2)}")
                await websocket.send(json.dumps(cmd))
                response = await websocket.recv()
                print(f"Response: {response}")
                await asyncio.sleep(3)  # Wait 3 seconds between commands
            
            print("\nAll commands executed successfully")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(execute_mcp_commands())