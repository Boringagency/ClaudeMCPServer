import asyncio
import websockets
import json

async def run_test():
    uri = "ws://localhost:8767"
    sequence = [
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "a"]},
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "c"]},
        {"type": "system", "action": "get_mouse_position"},
        {"type": "mouse", "action": "move", "x": 500, "y": 500},
        {"type": "mouse", "action": "click"},
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "v"]}
    ]
    
    async with websockets.connect(uri) as websocket:
        for cmd in sequence:
            await websocket.send(json.dumps(cmd))
            response = await websocket.recv()
            print(f"Command: {cmd}")
            print(f"Response: {response}\n")
            await asyncio.sleep(3)  # 3 second delay between commands

if __name__ == "__main__":
    asyncio.run(run_test())