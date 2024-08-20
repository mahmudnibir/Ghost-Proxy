# GoLogin_auto_proxy

This Python script automates the process of managing and running proxy profiles through GoLogin. The script can perform tasks such as adding profiles, pasting proxies, running profiles, clicking on links, and deleting profiles based on voice commands.

## Features

- **Profile Management**: Automatically adds the specified number of profiles.
- **Proxy Handling**: Reads proxies from a `proxy.txt` file and pastes them into the corresponding profiles.
- **Link Automation**: Pastes a predefined link into each profile and clicks on it.
- **Website Interaction**: Clicks on a specific point in the website once it loads.
- **Voice Command**: Listens for the voice command "delete all" to close and delete all profiles in GoLogin.

## Prerequisites

- **Python 3.12**
- **GoLogin**: Ensure that GoLogin is open and on the homepage before starting the script.
- **Python Libraries**: Install the required Python libraries by running:
  ```bash
  pip install pyautogui pyperclip pygetwindow SpeechRecognition asyncio pywinauto pypiwin32

## Usage
1. Setup: Adjust the coordinates for clicking on the website to fit your PC or laptop.
2. Prepare Proxy File: Ensure you have a proxy.txt file with sufficient proxies to match the number of profiles you intend to manage.
3. Run the Script: Execute the script. It will automate the following tasks:
--> Add profiles to GoLogin.
--> Paste proxies from the proxy.txt file.
--> Paste a predefined link into each profile.
--> Click on the link and interact with the website.
--> Voice Command: After completing the tasks, say "delete all" to          automatically close and delete the profiles in GoLogin.

## **Important Notes**
Window Activation: The script activates windows and interacts with them using PyAutoGUI, so ensure that no other programs interfere with the automated actions.
Timeouts: If the script fails to find an element within the timeout period, it will skip to the next task.

## **Example Workflow**
     Run the script with GoLogin open on the homepage.
     The script will add the specified number of profiles.
     It will paste the proxies into each profile.
     The script will then paste the link into each profile and interact with the website.
     After all tasks are completed, say "delete all" to remove the profiles.
     Customization

## **Customizations**-
You can customize the following variables in the script:

**profile_number**: The number of profiles to manage.
**first_link**: The link to be pasted and clicked in each profile.
**website_coordinates**: Change the coordinates for clicking on website according to your screen.
**time_after_update_proxy**: Change the time to remove non-american flag as you need. (e.g 20)
**time_after_run**: Change the time after running profile if needed. (e.g 15)

## **Troubleshooting**
Proxies Not Pasting: Ensure that the proxy.txt file has enough proxies and the format is correct.
Voice Commands Not Recognized: Ensure your microphone is working and configured correctly.