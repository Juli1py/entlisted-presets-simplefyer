from pynput import mouse
import keyboard
import threading

# Flag to control whether the listener is running
is_listening = False
listener = None
index = 0

# Get the soldier class input from the user
data = input("Select soldier class you want to make: ")

# Function to start the mouse listener
def start_listener():
    global listener, index
    # Generate the filename with the current index
    filename = f"{data}{index}.txt"
    
    with open(filename, "a") as file:  # Append mode to continue writing
        def on_click(x, y, button, pressed):
            if pressed and button == mouse.Button.left:
                # Print the coordinates and save to the file
                print(f"Mouse clicked at ({x}, {y})")
                file.write(f"Mouse clicked at ({x}, {y})\n")
                file.flush()  # Ensure the data is written immediately

        # Start listening for mouse events
        listener = mouse.Listener(on_click=on_click)
        listener.start()
        listener.join()

# Function to toggle the listener on and off with F1
def toggle_listener():
    global is_listening, listener, index

    print("Press F1 to start or stop the listener.")
    while True:
        keyboard.wait('F1')
        if not is_listening:
            print("Listening started. Click the left mouse button to log coordinates.")
            is_listening = True
            # Run the listener in a separate thread so it doesn't block the toggle
            threading.Thread(target=start_listener).start()
        else:
            print("Listening stopped. Press F1 to start again for making a new setup of the same class.")
            is_listening = False
            if listener:
                listener.stop()  # Stop the mouse listener
                listener = None
                # Increment index to create a new file next time
                index += 1

# Start the function to toggle the listener
toggle_listener()
