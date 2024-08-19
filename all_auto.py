import pyautogui
import time
import pyperclip
import pygetwindow as gw
import speech_recognition as sr

# Variables
profile_number = 10
time_diff_between_adding_proxy = 1.5
time_after_update_proxy = 20
time_after_run = 19
first_link = "https://tinyurl.com/Mehedi-1908-N5k"
window_title = "Browser Profiles - GoLogin 3.3.53 Jupiter"  # The title of the window to switch to
prefix = "profile"  # Define the prefix for the window titles you want to target

# Track the last activated window
last_activated_window = None

time.sleep(1)

def locate_and_click(image_name, confidence=0.8):
    
#     Locate an image on the screen and click it.
    
    location = pyautogui.locateCenterOnScreen(image_name, confidence=confidence)
    if location:
        pyautogui.click(location)
        print(f"Clicked on {image_name}")
    else:
        print(f"Image '{image_name}' not found on the screen.")

def activate_window_contains(keyword):
    global last_activated_window
    # Get all windows
    windows = gw.getWindowsWithTitle('')
    found = False

    for window in windows:
        if isinstance(window.title, str) and keyword in window.title:
            print(f"Activating window with title '{window.title}'")
            window.activate()  # Bring the window to the foreground
            time.sleep(3)  # Wait to ensure the window is activated
            last_activated_window = window
            found = True
            break

    if not found:
        print(f"No window with title containing '{keyword}' found.")

# Activate the window with "GoLogin" in the title
activate_window_contains("GoLogin")

# Add profiles
for _ in range(profile_number):
    locate_and_click('add_profile.png')
    time.sleep(time_diff_between_adding_proxy)

# Select all profiles
locate_and_click('select_all_profile.png')
time.sleep(1)

# Click on proxy
locate_and_click('proxy_button.png')
time.sleep(1)

# Function to read proxies from file and cut the required number
def get_proxies_from_file(file_path, num_proxies):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
        
    # Ensure there are enough proxies in the file
    if len(proxies) < num_proxies:
        print("Not enough proxies in the file.")
        return None

    # Get the required number of proxies
    selected_proxies = proxies[:num_proxies]
    remaining_proxies = proxies[num_proxies:]

    # Write the remaining proxies back to the file
    with open(file_path, 'w') as file:
        file.writelines(remaining_proxies)
    
    # Return the selected proxies as a single string to paste
    return ''.join(selected_proxies)

# File path of the proxy.txt
proxy_file_path = "proxy.txt"

# Get the proxies to paste
proxies_to_paste = get_proxies_from_file(proxy_file_path, profile_number)

if proxies_to_paste:
    pyperclip.copy(proxies_to_paste)  # Copy the proxies to clipboard

    # Paste proxy content
    locate_and_click('paste_proxy.png')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.8)
    locate_and_click('update_proxy.png')
    time.sleep(time_after_update_proxy)
else:
    print("Operation aborted due to insufficient proxies.")

# Run proxies
locate_and_click('select_all_profile.png')
time.sleep(2)
locate_and_click('run_proxy.png')
time.sleep(time_after_run)

# Copy link to clipboard
pyperclip.copy(first_link)

def activate_window(window):
    try:
        if window:
            window.activate()
            time.sleep(2)  # Wait to ensure the window is activated
        else:
            print("No window provided for activation.")
    except Exception as e:
        print(f"Failed to activate window: {window.title if window else 'Unknown'}, Error: {e}")

def paste_link_in_window(window, first_link):
    try:
        activate_window(window)  # Bring the window to the foreground
        pyperclip.copy(first_link)  # Copy the link to the clipboard
        pyautogui.hotkey('ctrl', 'v')  # Paste the link from clipboard
        pyautogui.press('enter')  # Press Enter to navigate to the link
        time.sleep(1)  # Wait to ensure the link is processed
    except Exception as e:
        print(f"Failed to paste link in window: {window.title if window else 'Unknown'}, Error: {e}")

def click_point_in_window(window, image_name):
    try:
        activate_window(window)  # Bring the window to the foreground
        locate_and_click(image_name)
        time.sleep(1.5)  # Wait to ensure the click is registered
    except Exception as e:
        print(f"Failed to click point in window: {window.title if window else 'Unknown'}, Error: {e}")

def click_point_in_website(window, image_name):
    try:
        activate_window(window)  # Bring the window to the foreground
        pyautogui.click(image_name)
        time.sleep(1.5)  # Wait to ensure the click is registered
    except Exception as e:
        print(f"Failed to click point in website: {window.title if window else 'Unknown'}, Error: {e}")

# Get all open windows
windows = gw.getAllWindows()

# Filter windows that start with the specified prefix
windows_to_target = [window for window in windows if window.title.lower().startswith(prefix.lower())]

# Paste the link in each filtered window
for window in windows_to_target:
    paste_link_in_window(window, first_link)

# Wait for 10 seconds before starting the click task
time.sleep(10)

# Click on the point in each filtered window
for window in windows_to_target:
    click_point_in_window(window, 'click_on_link.png')
time.sleep(15)

for window in windows_to_target:
    # click_point_in_website(window, 'click_on_website.png')
    # pyautogui.click(190, 360)
    click_point_in_website(window, (190, 360))

# Function to close all windows with a specific prefix
def close_windows_with_title_starting_with(prefix):
    # Get all open windows
    windows = gw.getAllWindows()

    # Filter windows that start with the specified prefix
    windows_to_close = [window for window in windows if window.title.lower().startswith(prefix.lower())]

    # Close each filtered window
    for window in windows_to_close:
        try:
            print(f"Closing window with title: {window.title}")
            window.close()  # Close the window
            time.sleep(0.2)  # Wait for a moment to ensure the window closes properly
        except Exception as e:
            print(f"Failed to close window with title: {window.title}, Error: {e}")

def activate_window(title):
    # Get the window with the specified title
    try:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            window = windows[0]  # Get the first window with the matching title
            print(f"Activating window with title '{title}'")
            window.activate()  # Bring the window to the foreground
            time.sleep(2)  # Wait to ensure the window is activated
        else:
            print(f"Window with title '{title}' not found.")
    except Exception as e:
        print(f"Error activating window with title '{title}': {e}")

# Function to handle "delete all" command
def handle_delete_all():
    global last_activated_window
    if last_activated_window:
        print(f"Activating last window with title '{last_activated_window.title}'")
        activate_window(last_activated_window.title)
        close_windows_with_title_starting_with(prefix)
    else:
        print("No window was activated previously.")

# Voice command functionality
def listen_for_commands():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Listening for command...")

    while True:
        with microphone as source:
            # Adjust the recognizer sensitivity to ambient noise and listen
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")

            if "delete all" in command.lower():
                handle_delete_all()
                activate_window(window_title)
                locate_and_click('delete_button.png')  # Replace with actual image name
                time.sleep(0.5)
                locate_and_click('yes_button.png')  # Replace with actual image name
                time.sleep(0.5)

                break  # Exit the loop after handling the command
            else:
                print("No valid command recognized.")
        
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError:
            print("Sorry, there was an issue with the request.")

# Call the function to listen for voice commands
listen_for_commands()
