"""
MIT License

Copyright (c) 2024 Nibir Mahmud

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import json
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
import win32con
import logging

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Ensure the logs directory exists
os.makedirs('logs', exist_ok=True)


profile_number = config['profile_number']
time_after_update_proxy = config['time_after_update_proxy']
time_after_run = config['time_after_run']
website_coordinates = tuple(config['website_coordinates'])
first_link = config['first_link']
window_title = config['window_title']
prefix = config['prefix']
proxy_file_path = config['proxy_file_path']
double_click = config['double_click']
n = config['loop_numbers']
scroll = config['scroll']

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Configure the logger for INFO level logs
info_handler = logging.FileHandler(config['log_file_info'])
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(formatter)
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.DEBUG)  # To ensure it captures INFO level messages
info_logger.addHandler(info_handler)
info_logger.propagate = False

# Configure the logger for DEBUG level logs
debug_handler = logging.FileHandler(config['log_file_debug'])
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)
debug_logger = logging.getLogger('debug_logger')
debug_logger.setLevel(logging.DEBUG)
debug_logger.addHandler(debug_handler)
debug_logger.propagate = False

# Configure the logger for WARNING level logs
warning_handler = logging.FileHandler(config['log_file_warning'])
warning_handler.setLevel(logging.WARNING)
warning_handler.setFormatter(formatter)
warning_logger = logging.getLogger('warning_logger')
warning_logger.setLevel(logging.WARNING)
warning_logger.addHandler(warning_handler)
warning_logger.propagate = False

# Configure the logger for ERROR level logs
error_handler = logging.FileHandler(config['log_file_error'])
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)
error_logger.propagate = False

engine = pyttsx3.init()

def speak(text):
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

# Track the last activated window
last_activated_window = None

def hide_window_from_taskbar(window_title_contains):
    # Enumerate all windows and find the one with the given title
    def enum_windows_callback(hwnd, windows):
        if window_title_contains.lower() in win32gui.GetWindowText(hwnd).lower():
            windows.append(hwnd)
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)

    for hwnd in windows:
        # Get the current extended window style
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        # Add the WS_EX_TOOLWINDOW style to hide it from the taskbar
        new_exstyle = exstyle | win32con.WS_EX_TOOLWINDOW
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
        # Show the window with the new style
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)

def restore_window(window_title_contains):
    # Enumerate all windows and find the one with the given title
    def enum_windows_callback(hwnd, windows):
        if window_title_contains.lower() in win32gui.GetWindowText(hwnd).lower():
            windows.append(hwnd)
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)

    for hwnd in windows:
        # Remove the WS_EX_TOOLWINDOW style to restore it to the taskbar
        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_exstyle = exstyle & ~win32con.WS_EX_TOOLWINDOW
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_exstyle)
        # Show the window normally
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)

def click_must(image_path, timeout=25):
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
            debug_logger.debug(f"Clicked on the button at {button_location}")
            return True  # Successfully clicked the button

        if time.time() - start_time > timeout:
            debug_logger.warning(f"Button did not appear within the timeout period for '{image_path}'. Skipping...")
            return False  # Timeout, move on to the next task

def click_if(image_path, timeout=50):
    image_path = f'buttons/{image_path}'
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)

            if button_location:
                pyautogui.click(button_location)
                debug_logger.debug(f"Clicked on the button at {button_location}")
                return True  # Successfully clicked the button

        except pyautogui.ImageNotFoundException:
            # If image not found, just wait and retry
            pass

        time.sleep(0.1)  # Wait 1 second before the next attempt

    warning_logger.warning(f"Button did not appear within the timeout period for '{image_path}'. Skipping...")
    return False  # Timeout, move on to the next task

def activate_window_contains(keyword):
    global last_activated_window
    windows = gw.getWindowsWithTitle('')
    found = False

    for window in windows:
        if isinstance(window.title, str) and keyword in window.title:
            debug_logger.debug(f"Activating window with title '{window.title}'")
            window.activate()  # Bring the window to the foreground
            time.sleep(1)  # Wait to ensure the window is activated
            last_activated_window = window
            found = True
            break

    if not found:
        error_logger.error(f"No window with title containing '{keyword}' found.")


def main_task():
    # Activate the window with "GoLogin" in the title
    activate_window_contains("GoLogin")

    def click_button(image_path, profile_number, timeout=15):
        image_path = f'buttons/{image_path}'
        for _ in range(profile_number):
            button_location = None
            start_time = time.time()
            while not button_location:
                try:
                    button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
                except pyautogui.ImageNotFoundException:
                    warning_logger.warning(f"Please open - {window_title} home page.Button not found. Retrying...")
                    time.sleep(1)  # Brief pause before retrying
                    continue

                if button_location:
                    pyautogui.click(button_location)
                    debug_logger.debug(f"Clicked on the button at {button_location}")
                    break  # Exit the loop once the button is clicked

                if time.time() - start_time > timeout:
                    debug_logger.debug("Still waiting for the button to appear...")
                    start_time = time.time()  # Reset the timer, continue waiting


    #waits till next button appears. this way it reduces time or time related errors.
    def wait_till_button_appear(image_path, extra_time=0, timeout=30):
        image_path = f'buttons/{image_path}'
        button_location = None
        start_time = time.time()
        
        while not button_location:
            try:
                button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
            except pyautogui.ImageNotFoundException:
                warning_logger.warning("Button not found. Retrying...")
                time.sleep(0.1)  # Brief pause before retrying
                continue
            
            if button_location:
                debug_logger.debug(f"Button found, waiting is over.")
                time.sleep(extra_time)
                break  # Exit the loop once the button is found
            
            if time.time() - start_time > timeout:
                error_logger.error("Timeout reached. Button did not appear.")
                return 0  # Return 0 if timeout is reached
            
    speak(f"adding {profile_number} profiles")
    click_button('add_profile.png', profile_number)
    wait_till_button_appear('add_profile.png')

    # Select all profiles
    click_must('select_all_profile.png')
    wait_till_button_appear('proxy_button.png', extra_time=0.1)

    click_must('proxy_button.png')
    wait_till_button_appear('paste_proxy.png', extra_time=0.1)

    # Function to read proxies from file and cut the required number
    def get_proxies_from_file(file_path, num_proxies):
        with open(file_path, 'r') as file:
            proxies = file.readlines()
            
        if len(proxies) < num_proxies:
            error_logger.error("Not enough proxies in the file.")
            return None

        selected_proxies = proxies[:num_proxies]
        remaining_proxies = proxies[num_proxies:]

        with open(file_path, 'w') as file:
            file.writelines(remaining_proxies)
        
        return ''.join(selected_proxies)

    # Get the proxies to paste
    proxies_to_paste = get_proxies_from_file(proxy_file_path, profile_number)

    if proxies_to_paste:
        pyperclip.copy(proxies_to_paste)  # Copy the proxies to clipboard
        click_must('paste_proxy.png')
        wait_till_button_appear('update_proxy.png', extra_time=0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        click_must('update_proxy.png')
        time.sleep(time_after_update_proxy)
    else:
        error_logger.error("Operation aborted due to insufficient proxies.")
        speak("Operation aborted due to insufficient proxies.")

    # Run proxies
    click_must('select_all_profile.png')
    wait_till_button_appear('run_proxy.png', extra_time=0.1)
    click_must('run_proxy.png')

    click_if('yes.png', timeout=2)
    time.sleep(time_after_run)

    # Copy link to clipboard
    pyperclip.copy(first_link)

    def activate_window(window):
        try:
            if window:
                window.activate()
                time.sleep(1.5)  # Wait to ensure the window is activated
            else:
                debug_logger.warning("No window provided for activation.")
        except Exception as e:
            error_logger.error(f"Failed to activate window: {window.title if window else 'Unknown'}, Error: {e}")

    def paste_and_press_enter(window_handle):
        try:
            app = Application(backend='uia').connect(handle=window_handle)
            window = app.window(handle=window_handle)
            window.type_keys('^v', pause=0.1)
            window.type_keys('{ENTER}', pause=0.2)
            debug_logger.debug(f"Pasted content and pressed Enter in window handle: {window_handle}")
        except Exception as e:
            error_logger.error(f"Failed to paste and press Enter in window handle: {window_handle}, Error: {e}")

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
            if click_if(image_name, timeout=20):
                debug_logger.debug(f"Clicked on '{image_name}' in the window '{window.title}'")
            else:
                warning_logger.warning(f"'{image_name}' button not found in window '{window.title}', skipping the task.")
            await asyncio.sleep(1)  # Wait asynchronously
        except Exception as e:
            error_logger.error(f"Failed to click point in window '{window.title}': {e}")

    async def click_point_in_website(window, coordinates):
        try:
            activate_window(window)
            pyautogui.click(coordinates)
            await asyncio.sleep(2)  # Wait asynchronously
        except Exception as e:
            error_logger.error(f"Failed to click point in website: {window.title if window else 'Unknown'}, Error: {e}")


    async def scroll_in_window(window, scroll_amount=-800):
        try:
            activate_window(window)  # Activate the window asynchronously
            pyautogui.scroll(scroll_amount)  # Scroll down
            await asyncio.sleep(2)  # Wait asynchronously for the scroll to take effect
        except Exception as e:
            error_logger.error(f"Failed to scroll in window: {window.title if window else 'Unknown'}, Error: {e}")

    async def main():
        windows = gw.getAllWindows()
        windows_to_target = [window for window in windows if window.title.lower().startswith(prefix.lower())]

        # Click the link in all windows
        for handle in window_handles:
            paste_and_press_enter(handle)

        # await asyncio.sleep(15)  # Wait for all links to be clicked

        link_click_tasks = []
        cross_click_tasks = []
        scroll_tasks = []
        for window in windows_to_target:
            cross_click_tasks.append(click_point_in_window(window, 'cross.png'))
            link_click_tasks.append(click_point_in_window(window, 'link.png'))
        
        await asyncio.gather(*cross_click_tasks)
        time.sleep(2)
        await asyncio.gather(*link_click_tasks)
        
        if double_click =="yes":

            await asyncio.sleep(30)  # Wait for the actions to complete

            website_click_tasks = []
            for window in windows_to_target:
                website_click_tasks.append(click_point_in_website(window, website_coordinates))

            await asyncio.gather(*website_click_tasks)

        if scroll =="yes":
            await asyncio.sleep(20)

            for window in windows_to_target:
                scroll_tasks.append(scroll_in_window(window))  # Add scrolling tasks

            # Wait for all scrolling tasks to complete
            await asyncio.gather(*scroll_tasks)


    # Run the asynchronous main function
    asyncio.run(main())

    def close_windows_with_title_starting_with(prefix):
        windows = gw.getAllWindows()
        windows_to_close = [window for window in windows if window.title.lower().startswith(prefix.lower())]

        for window in windows_to_close:
            try:
                info_logger.info(f"Task successfully executed: {window.title}")
                window.close()
                time.sleep(0.2)
            except Exception as e:
                error_logger.error(f"Failed to close window with title: {window.title}, Error: {e}")

    def activate_window(title):
        try:
            windows = gw.getWindowsWithTitle(title)
            if windows:
                window = windows[0]
                debug_logger.debug(f"Activating window with title '{title}'")
                window.activate()
                time.sleep(1)
            else:
                warning_logger.warning(f"Window with title '{title}' not found.")
        except Exception as e:
            error_logger.error(f"Error activating window with title '{title}': {e}")

    def handle_delete_all():
        global last_activated_window
        if last_activated_window:
            debug_logger.debug(f"Activating last window with title '{last_activated_window.title}'")
            activate_window(last_activated_window.title)
            close_windows_with_title_starting_with(prefix)
        else:
            error_logger.error("No window was activated previously.")

    def listen_for_commands():
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        debug_logger.debug("Listening for command...")

        while True:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            # Define the folder where screenshots will be saved
            screenshot_folder = "screenshots"
            os.makedirs(screenshot_folder, exist_ok=True)  # Create folder if it doesn't exist

            try:
                command = recognizer.recognize_google(audio)
                debug_logger.debug(f"You said: {command}")

                if "delete all" in command.lower():
                    speak("deleting all")
                    handle_delete_all()
                    activate_window(window_title)
                    time.sleep(0.1)
                    # hide_window_from_taskbar("Visual Studio Code")  # Hide VS Code
                    # debug_logger.debug("Visual Studio Code hidden")
                    # time.sleep(1)

                    # timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Use timestamp for unique filename
                    # screenshot_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
                    # screenshot = pyautogui.screenshot()
                    # screenshot.save(screenshot_path)  # Save the full-screen screenshot
                    # time.sleep(0.1)

                    # restore_window("Visual Studio Code")  # Restore VS Code after screenshots

                    wait_till_button_appear('delete_button.png', extra_time=0.1)
                    click_must('delete_button.png')
                    wait_till_button_appear('yes.png', extra_time=0.1)
                    click_must('yes.png')


                    # restore_window("Visual Studio Code")  # Restore VS Code after screenshots
                    # time.sleep(0.5)

                    break  # Exit the loop after handling
                elif "stop" in command.lower():
                    break
                else:
                    warning_logger.warning("No valid command recognized.")
            
            except sr.UnknownValueError:
                warning_logger.warning("Sorry, I did not understand the audio.")
            except sr.RequestError:
                error_logger.error("Network Connection Error . Check Network Connection and try again.")
                speak("Sorry, there was an issue with the request. Check your network connection and try again.")

    # Call the function to listen for voice commands
    listen_for_commands()

for i in range(n):
    try:
        main_task()  # Call the main function
        if i != n-1:  # Check if it's not the last iteration
            speak(f"Step {i + 1} completed.")
        else:  # Last iteration
            speak(f"Procedure completed, now you can run next proxies.")
        # time.sleep(1)  # Optional: Wait for a short period between iterations
    except Exception as e:
        error_logger.error(f"An error occurred during the loop execution: {e}")
        
