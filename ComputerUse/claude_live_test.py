import asyncio
import websockets
import json

async def run_claude_test():
    uri = "ws://localhost:8767"
    
    # Test sequence
    commands = [
        # Get initial mouse position
        {"type": "system", "action": "get_mouse_position"},
        
        # Move mouse to center and click
        {"type": "mouse", "action": "move", "x": 500, "y": 500},
        {"type": "mouse", "action": "click"},
        
        # Type a test message
        {"type": "keyboard", "action": "type", "text": "Hello from Claude! Testing MCP connection."},
        
        # Select all and copy
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "a"]},
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "c"]}
    ]
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to MCP server")
            
            for cmd in commands:
                print(f"\nSending command: {json.dumps(cmd, indent=2)}")
                await websocket.send(json.dumps(cmd))
                response = await websocket.recv()
                print(f"Server response: {response}")
                await asyncio.sleep(2)  # Wait between commands
                
            print("\nTest sequence completed successfully")
            
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == "__main__":
    asyncio.run(run_claude_test())