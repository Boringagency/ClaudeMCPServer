import pyautogui
import json

class KeyboardActions:
    @staticmethod
    async def perform_action(websocket, action_type, data):
        try:
            if action_type == 'hotkey':
                # Handle keyboard shortcuts
                keys = data.get('keys', [])
                if keys:
                    pyautogui.hotkey(*keys)
                    await websocket.send(json.dumps({
                        'status': 'success',
                        'action': 'hotkey',
                        'keys': keys
                    }))
            
            elif action_type == 'select_all':
                # Select all text (Command+A on macOS)
                pyautogui.hotkey('command', 'a')
                await websocket.send(json.dumps({
                    'status': 'success',
                    'action': 'select_all'
                }))
            
            elif action_type == 'copy':
                # Copy (Command+C on macOS)
                pyautogui.hotkey('command', 'c')
                await websocket.send(json.dumps({
                    'status': 'success',
                    'action': 'copy'
                }))
            
            elif action_type == 'paste':
                # Paste (Command+V on macOS)
                pyautogui.hotkey('command', 'v')
                await websocket.send(json.dumps({
                    'status': 'success',
                    'action': 'paste'
                }))
            
            elif action_type == 'shift_tab':
                # Navigate backwards
                pyautogui.hotkey('shift', 'tab')
                await websocket.send(json.dumps({
                    'status': 'success',
                    'action': 'shift_tab'
                }))
            
        except Exception as e:
            await websocket.send(json.dumps({
                'status': 'error',
                'action': action_type,
                'message': str(e)
            }))