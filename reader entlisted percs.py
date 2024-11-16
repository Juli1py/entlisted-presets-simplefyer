from pynput.mouse import Controller, Button
import keyboard
import threading
import time

# Flag to control whether the process should run
is_running = False

# Function to read coordinates from a text file and click at those positions
def read_and_click(file_path):
    global is_running
    mouse = Controller()
    
    try:
        # Open the file and read coordinates
        with open(file_path, "r") as file:
            for line in file:
                if not is_running:
                    print("Process stopped.")
                    break
                
                # Extract coordinates from each line
                if "Mouse clicked at" in line:
                    parts = line.strip().split("(")[-1].split(")")[0]
                    x, y = map(int, parts.split(", "))
                    
                    # Move the mouse to the coordinate and click
                    mouse.position = (x, y)
                    time.sleep(0.02)  # Optional delay to visualize the movement
                    mouse.click(Button.left, 1)
                    
                    print(f"Clicked at ({x}, {y})")
    
    except FileNotFoundError:
        print("The specified file was not found.")
    except ValueError:
        print("Error parsing coordinates. Ensure the file format is correct.")

# Function to toggle the process with F2
def toggle_process(file_path):
    global is_running

    print("Press F2 to start or stop the process.")
    while True:
        keyboard.wait('F2')
        if not is_running:
            print("Process started. Clicking will begin.")
            is_running = True
            # Run the click process in a separate thread
            threading.Thread(target=read_and_click, args=(file_path,), daemon=True).start()
        else:
            print("Process stopped.")
            is_running = False

# Get the file path from user input
filepath = input("ee the setup file name (without extension): ") + ".txt"
print(f"Using file: {filepath}")

# Start the toggle function
toggle_process(filepath)
