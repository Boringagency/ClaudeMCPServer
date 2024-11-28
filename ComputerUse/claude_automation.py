import asyncio
import websockets
import json

class ClaudeAutomation:
    def __init__(self, uri="ws://localhost:8767"):
        self.uri = uri
        
    async def execute_commands(self, commands):
        async with websockets.connect(self.uri) as websocket:
            results = []
            for cmd in commands:
                try:
                    await websocket.send(json.dumps(cmd))
                    response = await websocket.recv()
                    results.append(json.loads(response))
                    await asyncio.sleep(3)  # Delay between commands
                except Exception as e:
                    print(f"Error executing command {cmd}: {str(e)}")
                    results.append({"status": "error", "message": str(e)})
            return results

    async def select_all_and_copy(self):
        commands = [
            {"type": "keyboard", "action": "hotkey", "keys": ["command", "a"]},
            {"type": "keyboard", "action": "hotkey", "keys": ["command", "c"]}
        ]
        return await self.execute_commands(commands)

    async def get_mouse_position(self):
        commands = [
            {"type": "system", "action": "get_mouse_position"}
        ]
        return await self.execute_commands(commands)

    async def move_and_click(self, x, y):
        commands = [
            {"type": "mouse", "action": "move", "x": x, "y": y},
            {"type": "mouse", "action": "click"}
        ]
        return await self.execute_commands(commands)

    async def paste(self):
        commands = [
            {"type": "keyboard", "action": "hotkey", "keys": ["command", "v"]}
        ]
        return await self.execute_commands(commands)

async def main():
    automation = ClaudeAutomation()
    
    results = await automation.select_all_and_copy()
    print("Select and copy results:", json.dumps(results, indent=2))
    
    position = await automation.get_mouse_position()
    print("Mouse position:", json.dumps(position, indent=2))
    
    click_results = await automation.move_and_click(500, 500)
    print("Move and click results:", json.dumps(click_results, indent=2))
    
    paste_results = await automation.paste()
    print("Paste results:", json.dumps(paste_results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())