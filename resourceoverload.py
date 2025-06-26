import tkinter as tk
import random
import time

def create_window():
    """
    Creates a new Tkinter Toplevel window that does not auto-close.
    This version includes elements designed to be more resource-intensive.
    """
    # Create a new top-level window
    window = tk.Toplevel()
    window.title(f"Intensive Spam Window {random.randint(1000, 9999)}")

    # Randomly position the window on the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_pos = random.randint(50, screen_width - 450) # Adjusted for larger window
    y_pos = random.randint(50, screen_height - 350) # Adjusted for larger window
    window.geometry(f"400x300+{x_pos}+{y_pos}") # Make windows slightly larger

    # Add multiple labels and a text widget to increase initial resource load
    label1 = tk.Label(window, text="Intensive Window Activity!", font=("Arial", 14, "bold"), padx=10, pady=5)
    label1.pack()

    label2 = tk.Label(window, text="Watch resource usage...", font=("Arial", 10), padx=10, pady=2)
    label2.pack()

    text_area = tk.Text(window, height=3, width=40, wrap=tk.WORD, bg="lightgray")
    text_area.insert(tk.END, "This window is performing some 'intensive' operations...\n")
    text_area.pack(pady=5)
    text_area.config(state=tk.DISABLED) # Make it read-only

    # Add a canvas for dynamic drawing, which can be CPU intensive
    canvas = tk.Canvas(window, width=380, height=150, bg="white", bd=2, relief="sunken")
    canvas.pack(pady=5)

    def draw_random_shapes():
        """
        Draws multiple random shapes on the canvas to simulate intensive drawing.
        """
        if not window.winfo_exists(): # Check if the window still exists before drawing
            return

        canvas.delete("all") # Clear previous drawings

        num_shapes = random.randint(5, 20) # Draw 5 to 20 shapes
        for _ in range(num_shapes):
            shape_type = random.choice(["oval", "rectangle", "line"])
            color = "#%06x" % random.randint(0, 0xFFFFFF) # Random hex color

            x1, y1 = random.randint(0, 380), random.randint(0, 150)
            x2, y2 = random.randint(0, 380), random.randint(0, 150)

            if shape_type == "oval":
                canvas.create_oval(x1, y1, x2, y2, fill=color, outline="")
            elif shape_type == "rectangle":
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
            else: # line
                canvas.create_line(x1, y1, x2, y2, fill=color, width=random.randint(1, 5))

        # Schedule the next drawing update
        window.after(50, draw_random_shapes) # Update every 50 milliseconds

    # Start the continuous drawing
    draw_random_shapes()

    # Add a close button
    close_button = tk.Button(window, text="Close This Intensive Window", command=window.destroy, bg="red", fg="white")
    close_button.pack(pady=5)

def spam_windows_continuously():
    """
    Continuously spams Tkinter windows at a rate of approximately 5 per second,
    and the windows do not auto-close. Each window is now more resource-intensive.
    """
    # Delay in milliseconds between opening each window to achieve ~5 windows/second
    # 1000 ms / 5 windows = 200 ms per window
    delay_per_window = 200

    # Initialize the main Tkinter window (root). This is necessary for Toplevel windows.
    # We hide the root window as it's not directly part of the spamming.
    root = tk.Tk()
    root.withdraw() # Hide the main root window

    print("Starting continuous spam of more resource-intensive Tkinter windows (5 windows/second, no auto-close).")
    print("Close the terminal or use Ctrl+C to stop the program.")

    while True:
        create_window()
        # Process pending Tkinter events. This is crucial for the windows to appear
        # and for the `time.sleep` not to completely freeze the UI.
        root.update_idletasks()
        # Introduce a small delay before creating the next window
        time.sleep(delay_per_window / 1000.0) # Convert milliseconds to seconds

if __name__ == "__main__":
    spam_windows_continuously()
