
# **GoLogin_auto_proxy 🚀**

Welcome to **GoLogin_auto_proxy**! This Python script is designed to automate the management and execution of proxy profiles in GoLogin. With just a few commands, you can handle everything from profile creation to proxy assignment and web interactions, all controlled by your voice! 🎤✨

## **Features**

- **Profile Management:** Instantly add a specified number of profiles with zero manual input. 🆕
- **Proxy Handling:** Automatically read proxies from `proxy.txt` and assign them to your profiles. 📄🔗
- **Link Automation:** Paste and interact with a predefined link in each profile. 🔗💬
- **Website Interaction:** Click on a designated spot on the website after it loads. 🖱️🌐
- **Voice Commands:** Say "delete all" to close and delete all profiles effortlessly. 🗑️🎙️

## **Prerequisites**

- **Python 3.12:** Ensure you have Python 3.12 installed. 🐍
- **GoLogin:** Launch GoLogin and keep it on the homepage before running the script. 💻
- **Required Python Libraries:** Install the libraries using:

  ```bash
  pip install -r requirements.txt

  ```

## **Installation**

Follow these steps to set up and run the script:

```bash
# Clone the repository
git clone https://github.com/yourusername/GoLogin_auto_proxy.git

# Navigate to the project directory
cd GoLogin_auto_proxy

# Install the required libraries
pip install -r requirements.txt
```

## **Usage**

1. **Setup:** Adjust the coordinates for clicking on the website to match your screen resolution. 🖥️🔧
2. **Prepare Proxy File:** Create a `proxy.txt` file with enough proxies to correspond to the number of profiles you wish to manage. 📁🔢
3. **Run the Script:** Execute the script to perform the following:
   - Add profiles to GoLogin. ➕
   - Paste proxies from `proxy.txt` into the profiles. 📋🔄
   - Paste and click a predefined link in each profile. 🔗🖱️
   - Interact with the website. 🌐
   - **Voice Command:** After completing the tasks, say "delete all" to close and delete the profiles. 🗑️🎙️

## **Customization**

Personalize the script with these variables:

- **`profile_number`:** Number of profiles to manage. 🔢
- **`first_link`:** The link to be pasted and clicked in each profile. 🔗
- **`website_coordinates`:** Adjust the coordinates for clicking on the website according to your screen setup. 📍
- **`time_after_update_proxy`:** Modify the wait time after updating proxies (e.g., 20 seconds). ⏳
- **`time_after_run`:** Set the delay after running profiles (e.g., 15 seconds). ⏲️

## **Troubleshooting**

- **Proxies Not Pasting:** Ensure `proxy.txt` contains sufficient proxies and is properly formatted. 📄🔍
- **Voice Commands Not Recognized:** Verify your microphone is operational and correctly set up. 🎙️🔧

## **Example Workflow**

1. **Start the Script:** Make sure GoLogin is open on the homepage. 🏠
2. **Profile Addition:** The script will add the number of profiles you’ve specified. 🆕
3. **Proxy Assignment:** It will paste the proxies from your `proxy.txt` into each profile. 📋🔄
4. **Link Interaction:** The script will paste and interact with the link in each profile. 🔗🖱️
5. **Cleanup:** After completing all tasks, say "delete all" to remove the profiles. 🗑️

## **Find Screen Coordinates**

Use the following Python script to find screen coordinates with PyAutoGUI:

```python
import pyautogui

# Get the current mouse position
a = pyautogui.position()

# Print the current mouse position
print(a)
```

This script helps you identify exact screen coordinates for accurate interactions. Run it and position your cursor where you need the click or action to occur, and the script will output the coordinates. 📍🖱️

## **Known Issues**

- The script may not work properly on non-standard screen resolutions. 🖥️
- Voice commands might not be recognized in noisy environments. 🎙️

## **Contributing**

We welcome contributions! Feel free to fork the repository, make changes, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Contact**

If you have any questions, feel free to contact me at [nibirbbkr@gmail.com](mailto:nibirbbkr@gmail.com).
