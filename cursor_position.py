import pyautogui
import time

try:
    while True:
        # Get the current position of the mouse cursor
        x, y = pyautogui.position()
        print(f"Mouse Position: X={x}, Y={y}", end="\r")  # '\r' allows overwriting the line
        time.sleep(0.1)  # Sleep for 100 milliseconds to avoid flooding the output
except KeyboardInterrupt:
    print("\nStopped tracking mouse position.")
