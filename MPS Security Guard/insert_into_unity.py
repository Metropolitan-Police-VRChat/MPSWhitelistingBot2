from time import sleep
import keyboard as keyboard_input
import pyautogui as keyboard_output
import pyperclip as clipboard

def main():
    """
    Main function to automate the process of typing officer names into a specific application.
    """

    # Get the officer list from user input
    officer_list = input("Insert the officer list\n>>>").split(";")

    # Add an escape hotkey to exit the program
    keyboard_input.add_hotkey("esc", lambda: exit())

    # Wait for the user to press the spacebar
    keyboard_input.wait("space")

    # Type the number of officers into the application
    keyboard_output.write(str(len(officer_list)))
    keyboard_output.press("enter")
    keyboard_output.press("tab")

    # Loop through the officer list and type each name into the application
    for name in officer_list:
        clipboard.copy(name)
        sleep(.1)
        keyboard_output.hotkey("ctrl", "v")
        keyboard_output.press("tab")

# Call the main function
if __name__ == "__main__":
    main()
    
