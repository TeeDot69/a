import tkinter as tk
import random
import time

def create_window():
    """
    Creates a new Tkinter Toplevel window that does not auto-close.
    """
    # Create a new top-level window
    window = tk.Toplevel()
    window.title(f"Spam Window {random.randint(1000, 9999)}")

    # Randomly position the window on the screen
    # These values ensure the window stays mostly within a reasonable screen area.
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_pos = random.randint(50, screen_width - 350) # Ensure window is visible
    y_pos = random.randint(50, screen_height - 250) # Ensure window is visible
    window.geometry(f"300x200+{x_pos}+{y_pos}")

    # Add a label to the window
    label = tk.Label(window, text="Hello from a spam window!", padx=20, pady=20)
    label.pack()

    # Add a close button
    close_button = tk.Button(window, text="Close Me", command=window.destroy)
    close_button.pack(pady=10)

def spam_windows_continuously():
    """
    Continuously spams Tkinter windows at a rate of approximately 5 per second,
    and the windows do not auto-close.
    """
    # Delay in milliseconds between opening each window to achieve ~5 windows/second
    # 1000 ms / 5 windows = 200 ms per window
    delay_per_window = 200

    # Initialize the main Tkinter window (root). This is necessary for Toplevel windows.
    # We hide the root window as it's not directly part of the spamming.
    root = tk.Tk()
    root.withdraw() # Hide the main root window

    print("Starting continuous spam of Tkinter windows (5 windows/second, no auto-close).")
    print("Close the terminal or use Ctrl+C to stop the program.")

    while True:
        create_window()
        # Process pending Tkinter events. This is crucial for the windows to appear
        # and for the `time.sleep` not to completely freeze the UI.
        root.update_idletasks()
        # Introduce a small delay before creating the next window
        time.sleep(delay_per_window / 1000.0) # Convert milliseconds to seconds

    # The program will only reach here if the loop is broken (e.g., by an exception or signal)
    # The program will effectively run until manually stopped.


if __name__ == "__main__":
    # Call the continuous spamming function
    spam_windows_continuously()
