import sys
import pyautogui
import time
import win32gui
import pyperclip
import pygetwindow as gw
import speech_recognition as sr
import asyncio
from pywinauto import Application
import pyttsx3
from PyQt5 import QtWidgets, QtGui, QtCore
import win32con
from datetime import datetime
import os

# Initialize the text-to-speech engine
engine = pyttsx3.init()
website_coordinates = (190, 360)
prefix = "profile"
window_title = "Browser Profiles - GoLogin 3.3.53 Jupiter"

# Define utility functions
def speak(text):
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

# Track the last activated window
last_activated_window = None

time.sleep(1)

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

def locate_and_click(image_path, timeout=15):
    image_path = f'buttons/{image_path}'
    button_location = None
    start_time = time.time()
    while not button_location:
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if button_location:
                pyautogui.click(button_location)
                return True
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)
        if time.time() - start_time > timeout:
            return False

def activate_window_contains(keyword):
    windows = gw.getWindowsWithTitle('')
    for window in windows:
        if keyword in window.title:
            window.activate()
            time.sleep(1)
            return window
    return None

def get_proxies_from_file(file_path, num_proxies):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    if len(proxies) < num_proxies:
        return None
    selected_proxies = proxies[:num_proxies]
    remaining_proxies = proxies[num_proxies:]
    with open(file_path, 'w') as file:
        file.writelines(remaining_proxies)
    return ''.join(selected_proxies)

def click_button(image_path, profile_number, timeout=15):
    image_path = f'buttons/{image_path}'
    for _ in range(profile_number):
        button_location = None
        start_time = time.time()
        while not button_location:
            try:
                button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
                if button_location:
                    pyautogui.click(button_location)
                    break
            except pyautogui.ImageNotFoundException:
                time.sleep(0.1)
            if time.time() - start_time > timeout:
                start_time = time.time()

def wait_till_button_appear(image_path, extra_time=0, timeout=15):
    image_path = f'buttons/{image_path}'
    button_location = None
    start_time = time.time()
    while not button_location:
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
            if button_location:
                time.sleep(extra_time)
                return
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)
        if time.time() - start_time > timeout:
            return

def handle_delete_all():
    last_activated_window = activate_window_contains("GoLogin")
    if last_activated_window:
        close_windows_with_title_starting_with("profile")

def close_windows_with_title_starting_with(prefix):
    windows = gw.getAllWindows()
    windows_to_close = [window for window in windows if window.title.lower().startswith(prefix.lower())]
    for window in windows_to_close:
        window.close()
        time.sleep(0.2)

def paste_and_press_enter(window_handle):
    try:
        app = Application(backend='uia').connect(handle=window_handle)
        window = app.window(handle=window_handle)
        window.type_keys('^v', pause=0.1)
        window.type_keys('{ENTER}', pause=0.2)
    except Exception as e:
        print(f"Failed to paste and press Enter in window handle: {window_handle}, Error: {e}")

def activate_window(window):
    try:
        if window:
            window.activate()
            time.sleep(1.5)  # Wait to ensure the window is activated
        else:
            print("No window provided for activation.")
    except Exception as e:
        print(f"Failed to activate window: {window.title if window else 'Unknown'}, Error: {e}")

def enum_windows_callback(hwnd, windows):
    title = win32gui.GetWindowText(hwnd)
    if title.startswith("profile"):
        windows.append(hwnd)

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

    await asyncio.sleep(16)  # Wait for all links to be clicked

    link_click_tasks = []
    for window in windows_to_target:
        link_click_tasks.append(click_point_in_window(window, 'click_on_link.png'))

    await asyncio.gather(*link_click_tasks)
    
    await asyncio.sleep(18)  # Wait for the actions to complete

    website_click_tasks = []
    for window in windows_to_target:
        website_click_tasks.append(click_point_in_website(window, website_coordinates))

    await asyncio.gather(*website_click_tasks)

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
                time.sleep(0.1)
                hide_window_from_taskbar("Visual Studio Code")  # Hide VS Code
                print("Visual Studio Code hidden")
                time.sleep(3)

                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Use timestamp for unique filename
                screenshot_path = os.path.join(screenshot_folder, f"screenshot_{timestamp}.png")
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_path)  # Save the full-screen screenshot
                time.sleep(0.1)

                restore_window("Visual Studio Code")  # Restore VS Code after screenshots

                wait_till_button_appear('delete_button.png', extra_time=0.1)
                locate_and_click('delete_button.png')
                wait_till_button_appear('yes.png', extra_time=0.1)
                locate_and_click('yes.png')
                speak("procedure completed now you can run next proxies")

                restore_window("Visual Studio Code")  # Restore VS Code after screenshots
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

# GUI class definition
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('GoLogin Auto Proxy Manager')
        self.setWindowIcon(QtGui.QIcon('auto_GZ9_icon.ico'))
        self.setGeometry(100, 100, 450, 500)

        # Set a dark theme
        self.setStyleSheet("""
    QWidget {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                    stop: 0 #1e1e1e, stop: 1 #2c3e50);
        color: #ecf0f1;
        font-family: 'Segoe UI', sans-serif;
    }
    QLabel {
        font-size: 18px;
        color: #bdc3c7;
        margin-bottom: 15px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    QLineEdit, QSpinBox {
        background: rgba(44, 62, 80, 0.85);
        border: none;
        padding: 12px;
        border-radius: 20px;
        font-size: 16px;
        color: #ecf0f1;
        selection-background-color: #3498db;
        selection-color: #ffffff;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    QLineEdit:focus, QSpinBox:focus {
        background: rgba(44, 62, 80, 1);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
    }
    QPushButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                    stop: 0 #2980b9, stop: 1 #3498db);
        border: none;
        padding: 14px 20px;
        border-radius: 30px;
        font-size: 16px;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
        transition: background 0.3s ease, transform 0.2s ease;
    }
    QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, 
                                    stop: 0 #3498db, stop: 1 #2980b9);
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
    }
    QPushButton:pressed {
        background: #1f6db2;
        transform: scale(0.95);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    QLabel#error_message {
        color: #e74c3c;
        font-weight: bold;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
""")
        
        # Layout setup
        layout = QtWidgets.QVBoxLayout()

        # Labels and inputs
        self.profile_label = QtWidgets.QLabel('Number of Profiles:')
        self.profile_input = QtWidgets.QSpinBox()
        self.profile_input.setValue(10)

        self.update_time_label = QtWidgets.QLabel('Time After Update Proxy:')
        self.update_time_input = QtWidgets.QSpinBox()
        self.update_time_input.setValue(10)

        self.run_time_label = QtWidgets.QLabel('Time After Run:')
        self.run_time_input = QtWidgets.QSpinBox()
        self.run_time_input.setValue(20)

        self.link_label = QtWidgets.QLabel('Link:')
        self.link_input = QtWidgets.QLineEdit()
        self.link_input.setText("Paste link here")

        # Error message display
        self.error_message = QtWidgets.QLabel('')
        self.error_message.setObjectName("error_message")

        # Run button
        self.run_button = QtWidgets.QPushButton('Run')
        self.run_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.run_button.clicked.connect(self.run_task)

        # Adding widgets to layout
        layout.addWidget(self.profile_label)
        layout.addWidget(self.profile_input)
        layout.addWidget(self.update_time_label)
        layout.addWidget(self.update_time_input)
        layout.addWidget(self.run_time_label)
        layout.addWidget(self.run_time_input)
        layout.addWidget(self.link_label)
        layout.addWidget(self.link_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.error_message)

        self.setLayout(layout)

    def run_task(self):
        try:
            profile_number = self.profile_input.value()
            update_time = self.update_time_input.value()
            time_after_run = self.run_time_input.value()
            first_link = self.link_input.text()
            # window_title = self.window_title_input.text()
            # prefix = self.prefix_input.text()

            activate_window_contains("GoLogin")

            speak(f"Starting with {profile_number} profiles")
            click_button('add_profile.png', profile_number)
            wait_till_button_appear('add_profile.png')
            
            locate_and_click('select_all_profile.png')
            wait_till_button_appear('proxy_button.png', extra_time=0.1)
            locate_and_click('proxy_button.png')
            wait_till_button_appear('paste_proxy.png', extra_time=0.1)

            proxy_file_path = "proxy.txt"
            proxies_to_paste = get_proxies_from_file(proxy_file_path, profile_number)

            if proxies_to_paste:
                pyperclip.copy(proxies_to_paste)
                locate_and_click('paste_proxy.png')
                wait_till_button_appear('update_proxy.png', extra_time=0.1)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)
                locate_and_click('update_proxy.png')
                time.sleep(update_time)
            else:
                self.error_message.setText("Not enough proxies in the file.")
                return

            locate_and_click('select_all_profile.png')
            wait_till_button_appear('run_proxy.png', extra_time=0.1)
            locate_and_click('run_proxy.png')

            if locate_and_click('yes.png', timeout=2):
                print("Button Clicked...")

            time.sleep(time_after_run)

            # Copy link to clipboard
            pyperclip.copy(first_link)

            # Run the asynchronous main function
            asyncio.run(main())

            listen_for_commands()
            speak("Task completed.")
        except Exception as e:
            self.error_message.setText(f"An error occurred: {str(e)}")
            print(f"Error: {str(e)}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('auto_GZ9_icon.ico'))
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
