#!/Users/azhar/Desktop/others/claudeMCP/mcp-server-py/.env/bin/python
import sys
import os
import pyautogui
from datetime import datetime

def main():
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Set up save directory
    save_dir = "/Users/azhar/Desktop/others/claudeMCP/dump"
    os.makedirs(save_dir, exist_ok=True)
    
    # Take screenshot
    print("Taking screenshot...")
    screenshot = pyautogui.screenshot()
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screen_capture_{timestamp}.png"
    filepath = os.path.join(save_dir, filename)
    
    # Save screenshot
    screenshot.save(filepath)
    print(f"Screenshot saved to: {filepath}")

if __name__ == "__main__":
    main()