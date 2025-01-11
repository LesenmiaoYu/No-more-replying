import pyautogui
import time

# Continuously print the current mouse cursor's x and y coordinates
try:
    print("Move your mouse to see the coordinates. Press Ctrl+C to stop.")
    while True:
        x, y = pyautogui.position()  # Get current mouse position
        print(f"X: {x}, Y: {y}")  # Print coordinates on the same line
        time.sleep(0.1)  # Adjust delay to reduce CPU usage
except KeyboardInterrupt:
    print("\nStopped.")
