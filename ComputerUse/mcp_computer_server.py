import asyncio
import websockets
import json
import pyautogui
import base64
import io
from PIL import Image
from mss import mss
import time
import sys
import os
import pyperclip

class ComputerControlServer:
    def __init__(self, host='localhost', port=8767):
        self.host = host
        self.port = port
        self.sct = mss()
        pyautogui.FAILSAFE = False
        self.screen_width, self.screen_height = pyautogui.size()
        
    async def execute_action(self, action_data):
        """Execute various computer control actions"""
        action_type = action_data.get('type', '')
        try:
            if action_type == 'keyboard':
                return await self.handle_keyboard_action(action_data)
            elif action_type == 'mouse':
                return await self.handle_mouse_action(action_data)
            elif action_type == 'system':
                return await self.handle_system_action(action_data)
            elif action_type == 'text':
                return await self.handle_text_action(action_data)
            else:
                return {'status': 'error', 'message': 'Unknown action type'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    async def handle_keyboard_action(self, data):
        """Handle keyboard-related actions"""
        action = data.get('action', '')
        
        if action == 'type':
            text = data.get('text', '')
            pyautogui.write(text)
            return {'status': 'success', 'action': 'type', 'text': text}
            
        elif action == 'hotkey':
            keys = data.get('keys', [])
            pyautogui.hotkey(*keys)
            return {'status': 'success', 'action': 'hotkey', 'keys': keys}
            
        elif action == 'press':
            key = data.get('key', '')
            pyautogui.press(key)
            return {'status': 'success', 'action': 'press', 'key': key}

    async def handle_mouse_action(self, data):
        """Handle mouse-related actions"""
        action = data.get('action', '')
        
        if action == 'move':
            x = data.get('x', 0)
            y = data.get('y', 0)
            pyautogui.moveTo(x, y)
            return {'status': 'success', 'action': 'move', 'position': {'x': x, 'y': y}}
            
        elif action == 'click':
            button = data.get('button', 'left')
            clicks = data.get('clicks', 1)
            pyautogui.click(button=button, clicks=clicks)
            return {'status': 'success', 'action': 'click', 'button': button, 'clicks': clicks}
            
        elif action == 'drag':
            start_x = data.get('start_x', 0)
            start_y = data.get('start_y', 0)
            end_x = data.get('end_x', 0)
            end_y = data.get('end_y', 0)
            duration = data.get('duration', 0.5)
            pyautogui.dragTo(end_x, end_y, duration=duration)
            return {'status': 'success', 'action': 'drag'}

    async def handle_system_action(self, data):
        """Handle system-related actions"""
        action = data.get('action', '')
        
        if action == 'get_screen_size':
            return {
                'status': 'success',
                'action': 'get_screen_size',
                'width': self.screen_width,
                'height': self.screen_height
            }
            
        elif action == 'get_mouse_position':
            x, y = pyautogui.position()
            return {
                'status': 'success',
                'action': 'get_mouse_position',
                'x': x,
                'y': y
            }

    async def handle_text_action(self, data):
        """Handle text-related actions"""
        action = data.get('action', '')
        
        if action == 'copy':
            pyautogui.hotkey('command', 'a')
            await asyncio.sleep(0.1)
            pyautogui.hotkey('command', 'c')
            await asyncio.sleep(0.1)
            text = pyperclip.paste()
            return {
                'status': 'success',
                'action': 'copy',
                'text': text
            }
            
        elif action == 'paste':
            text = data.get('text', '')
            pyperclip.copy(text)
            pyautogui.hotkey('command', 'v')
            return {'status': 'success', 'action': 'paste'}

    async def handle_connection(self, websocket):
        print("New client connected")
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    response = await self.execute_action(data)
                    await websocket.send(json.dumps(response))
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        'status': 'error',
                        'message': 'Invalid JSON format'
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        'status': 'error',
                        'message': str(e)
                    }))
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            print("Client disconnected")

    async def start_server(self):
        if sys.platform == 'darwin':
            try:
                import Quartz
            except ImportError:
                print("Please install pyobjc-framework-Quartz for macOS support")
                sys.exit(1)

        server = websockets.serve(
            lambda ws: self.handle_connection(ws),
            self.host,
            self.port
        )
        
        print(f"Computer Control Server starting on ws://{self.host}:{self.port}")
        
        async with server:
            await asyncio.Future()

async def main():
    try:
        server = ComputerControlServer()
        await server.start_server()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())