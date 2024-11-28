#!/usr/bin/env python3
import pyautogui
import os
from datetime import datetime

# Set up save directory
save_dir = "/Users/azhar/Desktop/others/claudeMCP/dump"
os.makedirs(save_dir, exist_ok=True)

# Take screenshot
screenshot = pyautogui.screenshot()

# Generate filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"screen_capture_{timestamp}.png"
filepath = os.path.join(save_dir, filename)

# Save screenshot
screenshot.save(filepath)
print(f"Screenshot saved to: {filepath}")