import pyautogui
import time

# Load the reference images
us_flag_img = 'us_flag.png'  # Path to the US flag image
select_button_img = 'select_button.png'  # Path to the select button image

def locate_images():
    """Locate all instances of the US flags and select buttons on the screen."""
    try:
        us_flag_positions = list(pyautogui.locateAllOnScreen(us_flag_img, confidence=0.8))
        select_buttons = list(pyautogui.locateAllOnScreen(select_button_img, confidence=0.8))
        return us_flag_positions, select_buttons
    except Exception as e:
        print(f"Error locating images: {e}")
        return [], []

def get_button_positions(buttons):
    """Get the positions of detected buttons."""
    return [pyautogui.center(button) for button in buttons]

def click_button(button_x, button_y):
    """Click a button at the specified position."""
    pyautogui.click(button_x, button_y)
    print(f"Clicked button at: ({button_x}, {button_y})")
    # Move cursor away to avoid hover effects
    pyautogui.moveTo(button_x + 100, button_y + 100)  # Adjust as needed
    time.sleep(0.5)  # Short delay to ensure the click is registered

def scroll_down():
    """Scroll down to reveal more content."""
    pyautogui.scroll(-500)  # Adjust the scroll amount as needed
    print("Scrolled down")
    time.sleep(0.4)  # Wait for content to load after scrolling

def process_buttons():
    """Process and click select buttons that are not associated with US flags."""
    clicked_buttons = set()  # Track already clicked buttons

    while True:
        # Locate all images
        us_flag_positions, select_buttons = locate_images()

        if not select_buttons:
            print("No select buttons detected. Exiting.")
            break

        # Get button positions
        updated_positions = get_button_positions(select_buttons)

        # Click buttons
        any_clicked = False
        for button_x, button_y in updated_positions:
            if (button_x, button_y) in clicked_buttons:
                continue  # Skip already clicked buttons

            # Check if the button is non-US flag
            is_non_us_flag_button = True
            for flag in us_flag_positions:
                flag_x, flag_y = pyautogui.center(flag)
                if abs(button_y - flag_y) < 5:
                    is_non_us_flag_button = False
                    break

            if is_non_us_flag_button:
                click_button(button_x, button_y)
                clicked_buttons.add((button_x, button_y))  # Mark as clicked
                any_clicked = True
                break  # Exit loop to handle next button

        if not any_clicked:
            print("No more valid buttons detected. Exiting.")
            break

        # Scroll down to reveal more buttons
        scroll_down()

process_buttons()
