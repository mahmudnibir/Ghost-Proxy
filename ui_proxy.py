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

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# GUI class definition
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('GoLogin Auto Proxy Manager')
        self.setGeometry(100, 100, 450, 500)

        # Set a dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                font-size: 14px;
                margin-bottom: 5px;
            }
            QLineEdit, QSpinBox {
                background-color: #2d2d2d;
                border: 2px solid #3c3c3c;
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #5c5c5c;
            }
            QLabel#error_message {
                color: #ff4d4d;
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
        self.link_input.setText("https://tinyurl.com/Mehedi-2608-5K")

        self.window_title_label = QtWidgets.QLabel('Window Title:')
        self.window_title_input = QtWidgets.QLineEdit()
        self.window_title_input.setText("Browser Profiles - GoLogin 3.3.53 Jupiter")

        self.prefix_label = QtWidgets.QLabel('Prefix:')
        self.prefix_input = QtWidgets.QLineEdit()
        self.prefix_input.setText("profile")

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
        layout.addWidget(self.window_title_label)
        layout.addWidget(self.window_title_input)
        layout.addWidget(self.prefix_label)
        layout.addWidget(self.prefix_input)
        layout.addWidget(self.run_button)
        layout.addWidget(self.error_message)

        self.setLayout(layout)

    def speak(self, text):
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()

    def add_profiles(self, profile_number):
        try:
            self.speak(f"Adding {profile_number} profiles")
            click_button('add_profile.png', profile_number)
            wait_till_button_appear('add_profile.png')
        except Exception as e:
            self.error_message.setText(f"Error adding profiles: {str(e)}")

    def update_proxy(self, profile_number):
        try:
            locate_and_click('select_all_profile.png')
            wait_till_button_appear('proxy_button.png', extra_time=0.1)
            locate_and_click('proxy_button.png')
            wait_till_button_appear('paste_proxy.png', extra_time=0.1)

            # File path of the proxy.txt
            proxy_file_path = "proxy.txt"

            # Get the proxies to paste
            proxies_to_paste = get_proxies_from_file(proxy_file_path, profile_number)

            if proxies_to_paste:
                pyperclip.copy(proxies_to_paste)
                locate_and_click('paste_proxy.png')
                wait_till_button_appear('update_proxy.png', extra_time=0.1)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)
                locate_and_click('update_proxy.png')
                time.sleep(self.update_time_input.value())
            else:
                self.error_message.setText("Operation aborted due to insufficient proxies.")
        except Exception as e:
            self.error_message.setText(f"Error updating proxy: {str(e)}")

    def run_task(self):
        try:
            profile_number = self.profile_input.value()
            time_after_update_proxy = self.update_time_input.value()
            time_after_run = self.run_time_input.value()
            first_link = self.link_input.text()
            window_title = self.window_title_input.text()
            prefix = self.prefix_input.text()

            activate_window_contains("GoLogin")

            # Add profiles
            self.add_profiles(profile_number)

            # Update proxy
            self.update_proxy(profile_number)

            # Run proxies
            locate_and_click('select_all_profile.png')
            wait_till_button_appear('run_proxy.png', extra_time=0.1)
            locate_and_click('run_proxy.png')

            time.sleep(time_after_run)

            # Copy link to clipboard
            pyperclip.copy(first_link)

            # Handle the main async tasks
            asyncio.run(self.main_async_tasks(prefix, window_title))

        except Exception as e:
            self.error_message.setText(f"Error running task: {str(e)}")

    async def main_async_tasks(self, prefix, window_title):
        try:
            windows = gw.getAllWindows()
            windows_to_target = [window for window in windows if window.title.lower().startswith(prefix.lower())]

            # Click the link in all windows
            for handle in windows_to_target:
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
        except Exception as e:
            self.error_message.setText(f"Error in async tasks: {str(e)}")


# Your existing methods for clicking buttons, activating windows, etc.
# Note: Include all your existing functions such as locate_and_click, activate_window, etc. below this class.

def locate_and_click(image_path, timeout=15):
    button_location = None
    start_time = time.time()

    while not button_location:
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)
            continue

        if button_location:
            pyautogui.click(button_location)
            print(f"Clicked on the button at {button_location}")
            return True

        if time.time() - start_time > timeout:
            print(f"Button did not appear within the timeout period for '{image_path}'. Skipping...")
            return False

def activate_window_contains(keyword):
    global last_activated_window
    windows = gw.getWindowsWithTitle('')
    found = False

    for window in windows:
        if isinstance(window.title, str) and keyword in window.title:
            print(f"Activating window with title '{window.title}'")
            window.activate()
            time.sleep(1)
            last_activated_window = window
            found = True
            break

    if not found:
        print(f"No window with title containing '{keyword}' found.")

def click_button(image_path, profile_number, timeout=15):
    for _ in range(profile_number):
        button_location = None
        start_time = time.time()
        while not button_location:
            try:
                button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.7)
            except pyautogui.ImageNotFoundException:
                print("Button not found. Retrying...")
                time.sleep(0.1)
                continue

            if button_location:
                pyautogui.click(button_location)
                print(f"Clicked on the button at {button_location}")
                break

            if time.time() - start_time > timeout:
                print("Still waiting for button. Timeout period exceeded.")
                return

def wait_till_button_appear(image_path, extra_time=0):
    button_location = None
    while not button_location:
        try:
            button_location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        except pyautogui.ImageNotFoundException:
            time.sleep(0.1)
            continue

    if button_location:
        time.sleep(extra_time)
        print(f"Button appeared at {button_location}")
        return button_location

def get_proxies_from_file(file_path, num_proxies):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    if len(proxies) < num_proxies:
        print(f"Not enough proxies available. Needed: {num_proxies}, Found: {len(proxies)}")
        return None

    selected_proxies = proxies[:num_proxies]
    return ''.join(selected_proxies)

def paste_and_press_enter(window_handle):
    window_handle.activate()
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')

def click_point_in_window(window, image_path):
    window.activate()
    time.sleep(1)
    locate_and_click(image_path)

def click_point_in_website(window, coordinates):
    window.activate()
    time.sleep(1)
    pyautogui.click(coordinates)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
