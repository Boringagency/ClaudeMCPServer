import asyncio
import websockets
import json
import time
import pyautogui

async def copy_and_navigate():
    uri = "ws://localhost:8767"
    print("Connecting to", uri)
    
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected to Computer Control Server")

            # 1. Get screen size for reference
            await websocket.send(json.dumps({
                'command': 'get_screen_size'
            }))
            response = await websocket.recv()
            screen_info = json.loads(response)
            print(f"Screen size: {screen_info}")

            # 2. Simulate Shift+Tab (navigate backwards)
            print("\nPerforming Shift+Tab...")
            pyautogui.hotkey('shift', 'tab')
            await asyncio.sleep(1)

            # 3. Select text (click and drag)
            print("\nSelecting text...")
            await websocket.send(json.dumps({
                'command': 'drag',
                'start_x': 200,
                'start_y': 200,
                'end_x': 400,
                'end_y': 200
            }))
            await asyncio.sleep(1)

            # 4. Copy selected text (Command+C on macOS)
            print("\nCopying text...")
            pyautogui.hotkey('command', 'c')
            await asyncio.sleep(1)

            print("Operations completed successfully")
            
    except websockets.exceptions.ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"Test error: {str(e)}")

async def main():
    print("Starting Copy and Navigation Test...")
    try:
        await copy_and_navigate()
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Main error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())