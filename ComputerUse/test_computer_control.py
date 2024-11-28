import asyncio
import websockets
import json
import time

async def test_computer_control():
    uri = "ws://localhost:8767"
    print("Connecting to", uri)
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to Computer Control Server")

            # Example 1: Get screen size
            request = {
                'command': 'get_screen_size'
            }
            print(f"Sending request: {request}")
            await websocket.send(json.dumps(request))

            response = await websocket.recv()
            print(f"Received response: {response}")
            
            # Example 2: Move mouse in a square pattern
            points = [
                (100, 100),
                (300, 100),
                (300, 300),
                (100, 300),
                (100, 100)
            ]
            
            print("\nMoving mouse in a square pattern...")
            for x, y in points:
                request = {
                    'command': 'move',
                    'x': x,
                    'y': y
                }
                print(f"Moving to: ({x}, {y})")
                await websocket.send(json.dumps(request))
                await asyncio.sleep(1)

            # Example 3: Perform click
            print("\nPerforming click...")
            request = {
                'command': 'click',
                'button': 'left',
                'clicks': 1
            }
            await websocket.send(json.dumps(request))
            await asyncio.sleep(1)

            # Example 4: Scroll test
            print("\nTesting scroll...")
            request = {
                'command': 'scroll',
                'amount': 100
            }
            await websocket.send(json.dumps(request))
            await asyncio.sleep(1)

            print("Test completed successfully")
            
    except websockets.exceptions.ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"Test error: {str(e)}")

async def main():
    print("Starting Computer Control Test...")
    try:
        await test_computer_control()
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Main error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())