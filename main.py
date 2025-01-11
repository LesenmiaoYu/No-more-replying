import pyautogui
import cv2
import numpy as np
import time
import pyperclip
import pygetwindow as gw
from PIL import Image
import openai

# OpenAI API Key
openai.api_key = "PUT YOUR OWN HERE"

# Function to generate a response using ChatGPT
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and playful human who responds succinctly to text messages, pretending to be the user, and never revealing that you are an AI."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        print(f"OpenAI API Error: {e}")
        return "Sorry, I couldn't generate a response."

# Function to find the position and dimensions of a window by its title
def find_window_position(window_title):
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            window = windows[0]  # Use the first matching window
            return window.left, window.top, window.width, window.height
        else:
            print(f"Window with title '{window_title}' not found.")
            return None
    except Exception as e:
        print(f"Error finding window: {e}")
        return None

# Function to capture a screenshot of a specific area
def capture_screen(area):
    screenshot = pyautogui.screenshot(region=area)
    return screenshot  # Return the PIL image directly

# Function to save the captured screenshot to a file
def save_screenshot(image, filename):
    image.save(filename)  # Use the PIL save method
    print(f"Screenshot saved as: {filename}")

# Function to check for differences between images
def images_are_different(current_image, previous_image):
    # If there's no previous image, assume no difference
    if previous_image is None:
        return False

    # Convert PIL images to NumPy arrays for comparison
    current_array = np.array(current_image)
    previous_array = np.array(previous_image)

    # Calculate pixel-wise absolute difference
    difference = cv2.absdiff(current_array, previous_array)

    # Calculate the total difference as the sum of all pixel differences
    diff_sum = np.sum(difference)
    print(f"Difference sum: {diff_sum}")  # Debugging log

    # Increase threshold by 5x to reduce flickering
    threshold = 1000000  # Adjust this as needed (5x the original 200,000)
    return diff_sum > threshold

# Main script
def main():
    # Clear the clipboard
    pyperclip.copy("")
    print("Clipboard cleared.")

    window_title = "WeChat"  # Replace with the title of your target window
    window_position = find_window_position(window_title)

    if not window_position:
        print("Unable to find the specified window.")
        return

    # Allow user 5 seconds to make changes
    print("You have 5 seconds to prepare the application...")
    time.sleep(5)

    monitor_area = (window_position[0], window_position[1], window_position[2], window_position[3])

    # Capture the first image to initialize monitoring without triggering a change
    previous_image = capture_screen(monitor_area)
    print("Initial image captured. Starting monitoring...")

    # Positions for actions
    select_text_position = (366, 1231)  # Adjust as needed
    input_text_position = (343, 1320)  # Adjust as needed

    while True:
        # Capture the current screenshot
        current_image = capture_screen(monitor_area)

        # Save the current screenshot for visual observation
        save_screenshot(current_image, "current_image.png")

        # Check for changes
        if images_are_different(current_image, previous_image):
            print("Change detected in monitored area.")

            # Save the previous screenshot (if it exists) for comparison
            if previous_image is not None:
                save_screenshot(previous_image, "previous_image.png")

            # Step 1: Move to text area and double-click to select text
            pyautogui.click(*select_text_position, clicks=2, interval=0.25)  # Double-click
            pyautogui.hotkey("ctrl", "c")  # Copy to clipboard

            # Step 2: Read copied text
            text = pyperclip.paste().strip()
            print(f"Copied text: {text}")

            if text:
                # Step 3: Generate a response using ChatGPT with the custom prompt
                prompt = f"Here is a text my friend sent me: '{text}'. Respond to it as if you were me, playfully and friendly, and keep the response succinct."
                response = generate_response(prompt)
                print(f"Generated response: {response}")

                # Step 4: Move to input box and paste the response
                pyautogui.click(*input_text_position)
                pyperclip.copy(response)
                pyautogui.hotkey("ctrl", "v")  # Paste
                pyautogui.press("enter")  # Send message

                # Step 5: Clear the clipboard after sending
                pyperclip.copy("")
                print("Clipboard cleared after sending the message.")

                # Step 6: Capture the screen again to reset the previous image
                previous_image = capture_screen(monitor_area)
                print("Updated previous image after sending the message.")

            # Pause briefly to ensure the UI has stabilized
            print("Pausing monitoring for 20 seconds...")
            time.sleep(20)
        else:
            print("No change detected.")

        time.sleep(0.5)  # Adjust delay as needed for responsiveness

if __name__ == "__main__":
    main()
