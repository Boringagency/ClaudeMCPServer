import asyncio
import websockets
import json

class ClaudeComputerClient:
    def __init__(self, uri="ws://localhost:8767"):
        self.uri = uri
        
    async def send_command(self, command_data):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(json.dumps(command_data))
            response = await websocket.recv()
            return json.loads(response)
            
    async def execute_sequence(self, commands):
        results = []
        for cmd in commands:
            result = await self.send_command(cmd)
            results.append(result)
            await asyncio.sleep(3)
        return results

async def main():
    client = ClaudeComputerClient()
    commands = [
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "a"]},
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "c"]},
        {"type": "system", "action": "get_mouse_position"},
        {"type": "mouse", "action": "move", "x": 500, "y": 500},
        {"type": "mouse", "action": "click"},
        {"type": "keyboard", "action": "hotkey", "keys": ["command", "v"]}
    ]
    
    try:
        results = await client.execute_sequence(commands)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())