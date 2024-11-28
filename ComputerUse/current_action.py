import asyncio
import websockets
import json

async def test_connection():
    uri = "ws://localhost:8767"
    # First let's check system info
    command = {"type": "system", "action": "get_mouse_position"}
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to MCP server")
            await websocket.send(json.dumps(command))
            response = await websocket.recv()
            print(f"Current mouse position: {response}")
            
            # Now move mouse to center
            move_command = {
                "type": "mouse", 
                "action": "move", 
                "x": 500, 
                "y": 500
            }
            await websocket.send(json.dumps(move_command))
            move_response = await websocket.recv()
            print(f"Move result: {move_response}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())