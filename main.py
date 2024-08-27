import pyautogui
import time
import win32gui
import pyperclip
import pygetwindow as gw
import speech_recognition as sr
import asyncio
from pywinauto import Application
import pyttsx3
import os
from datetime import datetime

# Variables
profile_number = 10  # select as much as you need
time_after_update_proxy = 10  # time to delete flags
time_after_run = 20 # time to finish run
website_coordinates = (190, 360)  # position where to click at website
first_link = "https://tinyurl.com/Mehedi-2708-5K"  # link to paste after run
window_title = "Browser Profiles - GoLogin 3.3.53 Jupiter"  # The title of the window to switch to
prefix = "profile"  # Define the prefix for the window titles you want to target


# Initialize the text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

# Track the last activated window
last_activated_window = None

time.sleep(1)

def locate_and_click(image_path, timeout=15):
    image_path = f'buttons/{image_path}'
    button_location = None
    start_time = time.time()

    while not button_location:
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)  # Brief pause before retrying
            continue

        if button_location:
            pyautogui.click(button_location)
            print(f"Clicked on the button at {button_location}")
            return True  # Successfully clicked the button

        if time.time() - start_time > timeout:
            print(f"Button did not appear within the timeout period for '{image_path}'. Skipping...")
            return False  # Timeout, move on to the next task

def activate_window_contains(keyword):
    global last_activated_window
    windows = gw.getWindowsWithTitle('')
    found = False

    for window in windows:
        if isinstance(window.title, str) and keyword in window.title:
            print(f"Activating window with title '{window.title}'")
            window.activate()  # Bring the window to the foreground
            time.sleep(1)  # Wait to ensure the window is activated
            last_activated_window = window
            found = True
            break

    if not found:
        print(f"No window with title containing '{keyword}' found.")

# Activate the window with "GoLogin" in the title
activate_window_contains("GoLogin")

# def click_if_exists(image_path, timeout=5):
#     start_time = time.time()
#     while time.time() - start_time < timeout:
#         button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
#         if button_location:
#             pyautogui.click(button_location)
#             print(f"Clicked on '{image_path}' button.")
#             return True
#         time.sleep(1)  # Wait before retrying
#     return False

def click_button(image_path, profile_number, timeout=15):
    image_path = f'buttons/{image_path}'
    for _ in range(profile_number):
        button_location = None
        start_time = time.time()
        while not button_location:
            try:
                button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
            except pyautogui.ImageNotFoundException:
                print("Button not found. Retrying...")
                time.sleep(0.1)  # Brief pause before retrying
                continue

            if button_location:
                pyautogui.click(button_location)
                print(f"Clicked on the button at {button_location}")
                break  # Exit the loop once the button is clicked

            if time.time() - start_time > timeout:
                print("Still waiting for the button to appear...")
                start_time = time.time()  # Reset the timer, continue waiting


#waits till next button appears. this way it reduces time or time related errors.
def wait_till_button_appear(image_path, extra_time=0, timeout=15):
    image_path = f'buttons/{image_path}'
    button_location = None
    start_time = time.time()
    
    while not button_location:
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
        except pyautogui.ImageNotFoundException:
            print("Button not found. Retrying...")
            time.sleep(0.1)  # Brief pause before retrying
            continue
        
        if button_location:
            print(f"Button found, waiting is over.")
            time.sleep(extra_time)
            break  # Exit the loop once the button is found
        
        if time.time() - start_time > timeout:
            print("Timeout reached. Button did not appear.")
            return 0  # Return 0 if timeout is reached
        
speak(f"adding {profile_number} profiles")
click_button('add_profile.png', profile_number)
wait_till_button_appear('add_profile.png')

# Select all profiles
locate_and_click('select_all_profile.png')
wait_till_button_appear('proxy_button.png', extra_time=0.1)
# time.sleep(0.5)

# Click on proxy
locate_and_click('proxy_button.png')
# speak(f"pasting {profile_number} proxies")
wait_till_button_appear('paste_proxy.png', extra_time=0.1)
# time.sleep(0.5)

# Function to read proxies from file and cut the required number
def get_proxies_from_file(file_path, num_proxies):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
        
    if len(proxies) < num_proxies:
        print("Not enough proxies in the file.")
        return None

    selected_proxies = proxies[:num_proxies]
    remaining_proxies = proxies[num_proxies:]

    with open(file_path, 'w') as file:
        file.writelines(remaining_proxies)
    
    return ''.join(selected_proxies)

# File path of the proxy.txt
proxy_file_path = "proxy.txt"

# Get the proxies to paste
proxies_to_paste = get_proxies_from_file(proxy_file_path, profile_number)

if proxies_to_paste:
    pyperclip.copy(proxies_to_paste)  # Copy the proxies to clipboard
    locate_and_click('paste_proxy.png')
    wait_till_button_appear('update_proxy.png', extra_time=0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)
    locate_and_click('update_proxy.png')
    time.sleep(time_after_update_proxy)
else:
    print("Operation aborted due to insufficient proxies.")

# Run proxies
locate_and_click('select_all_profile.png')
wait_till_button_appear('run_proxy.png', extra_time=0.1)
# time.sleep(0.5)
locate_and_click('run_proxy.png')


# if locate_and_click('yes.png', timeout=2):
#     print("Button Clicked...")


# # Check and click 'Yes' button if it appears
# if click_if_exists('yes.png'):
#     print("Clicked 'Yes' button.")
#     # Continue with the rest of the code after clicking 'Yes'
# else:
#     print("'Yes' button did not appear.")
# #     # Continue with the rest of the code if 'Yes' button does not appear

time.sleep(time_after_run)

# Copy link to clipboard
pyperclip.copy(first_link)

def activate_window(window):
    try:
        if window:
            window.activate()
            time.sleep(1.5)  # Wait to ensure the window is activated
        else:
            print("No window provided for activation.")
    except Exception as e:
        print(f"Failed to activate window: {window.title if window else 'Unknown'}, Error: {e}")

def paste_and_press_enter(window_handle):
    try:
        app = Application(backend='uia').connect(handle=window_handle)
        window = app.window(handle=window_handle)
        window.type_keys('^v', pause=0.1)
        window.type_keys('{ENTER}', pause=0.2)
        print(f"Pasted content and pressed Enter in window handle: {window_handle}")
    except Exception as e:
        print(f"Failed to paste and press Enter in window handle: {window_handle}, Error: {e}")

def enum_windows_callback(hwnd, windows):
    title = win32gui.GetWindowText(hwnd)
    if title.startswith("profile"):
        windows.append(hwnd)

# Get all window handles
window_handles = []
win32gui.EnumWindows(enum_windows_callback, window_handles)

async def click_point_in_window(window, image_name):
    try:
        activate_window(window)
        if locate_and_click(image_name, timeout=10):
            print(f"Clicked on '{image_name}' in the window '{window.title}'")
        else:
            print(f"'{image_name}' button not found in window '{window.title}', skipping the task.")
        await asyncio.sleep(1)  # Wait asynchronously
    except Exception as e:
        print(f"Failed to click point in window '{window.title}': {e}")

async def click_point_in_website(window, coordinates):
    try:
        activate_window(window)
        pyautogui.click(coordinates)
        await asyncio.sleep(2)  # Wait asynchronously
    except Exception as e:
        print(f"Failed to click point in website: {window.title if window else 'Unknown'}, Error: {e}")

async def main():
    windows = gw.getAllWindows()
    windows_to_target = [window for window in windows if window.title.lower().startswith(prefix.lower())]

    # Click the link in all windows
    for handle in window_handles:
        paste_and_press_enter(handle)

    await asyncio.sleep(12)  # Wait for all links to be clicked

    link_click_tasks = []
    for window in windows_to_target:
        link_click_tasks.append(click_point_in_window(window, 'click_on_link.png'))

    await asyncio.gather(*link_click_tasks)
    
    await asyncio.sleep(18)  # Wait for the actions to complete

    website_click_tasks = []
    for window in windows_to_target:
        website_click_tasks.append(click_point_in_website(window, website_coordinates))

    await asyncio.gather(*website_click_tasks)

# Run the asynchronous main function
asyncio.run(main())

def close_windows_with_title_starting_with(prefix):
    windows = gw.getAllWindows()
    windows_to_close = [window for window in windows if window.title.lower().startswith(prefix.lower())]

    for window in windows_to_close:
        try:
            print(f"Closing window with title: {window.title}")
            window.close()
            time.sleep(0.2)
        except Exception as e:
            print(f"Failed to close window with title: {window.title}, Error: {e}")

def activate_window(title):
    try:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            window = windows[0]
            print(f"Activating window with title '{title}'")
            window.activate()
            time.sleep(1)
        else:
            print(f"Window with title '{title}' not found.")
    except Exception as e:
        print(f"Error activating window with title '{title}': {e}")

def handle_delete_all():
    global last_activated_window
    if last_activated_window:
        print(f"Activating last window with title '{last_activated_window.title}'")
        activate_window(last_activated_window.title)
        close_windows_with_title_starting_with(prefix)
    else:
        print("No window was activated previously.")

def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for command...")

    while True:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        # Define the folder where screenshots will be saved
        screenshot_folder = "screenshots"
        os.makedirs(screenshot_folder, exist_ok=True)  # Create folder if it doesn't exist

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if "delete all" in command.lower():
                speak("deleting all")
                handle_delete_all()
                activate_window(window_title)
                time.sleep(3)
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Use timestamp for unique filename
                screenshot_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_path)  # Save the full-screen screenshot
                time.sleep(0.5)
                wait_till_button_appear('delete_button.png', extra_time=0.1)
                locate_and_click('delete_button.png')
                wait_till_button_appear('yes.png', extra_time=0.1)
                locate_and_click('yes.png')
                speak("procedure completed now you can run next proxies")
                time.sleep(0.5)

                break  # Exit the loop after handling
            elif "stop" in command.lower():
                break
            else:
                print("No valid command recognized.")
        
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError:
            print("Sorry, there was an issue with the request. Check your network connection and try again.")
            speak("Sorry, there was an issue with the request. Check your network connection and try again.")

# Call the function to listen for voice commands
listen_for_commands()
