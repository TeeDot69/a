import tkinter as tk
import random
import time

# List to keep track of all active windows to prevent them from being garbage collected
# prematurely, especially with scheduled tasks.
active_windows = []
batch_counter = 0 # Global counter for batches created

def create_window():
    """
    Creates a new Tkinter Toplevel window with a simulated 3D ball animation
    and a mechanism for the window itself to move around.
    """
    window = tk.Toplevel()
    window.title(f"Dynamic Intensive Spam Window {random.randint(1000, 9999)}")

    # Initial random position for the window
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 400
    window_height = 300
    x_pos = random.randint(50, screen_width - window_width - 50)
    y_pos = random.randint(50, screen_height - window_height - 50)
    window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    # Store movement directions and animation state directly on the window object
    # This helps encapsulate state for each individual window.
    window.x_dir = random.choice([-5, 5]) # Window movement speed and direction
    window.y_dir = random.choice([-5, 5])

    # --- Changes for multiple balls ---
    num_balls = 10 # Number of balls to display in each window
    window.balls_data = [] # List to store data for each ball

    for _ in range(num_balls):
        window.balls_data.append({
            'radius': random.randint(40, 60), # Initial radius for each 3D ball
            'radius_direction': random.choice([-1, 1]), # 1 for increasing, -1 for decreasing
            'x': random.randint(50, window_width - 50), # Ball's initial X position on canvas
            'y': random.randint(50, window_height - 150), # Ball's initial Y position on canvas
            'dx': random.choice([-3, 3]), # Ball's movement speed on canvas
            'dy': random.choice([-3, 3]),
            'color_offset': random.randint(0, 20) # For unique colors
        })
    # --- End changes for multiple balls ---

    # Add labels and text area (for resource intensity)
    label1 = tk.Label(window, text="Intensive & Dynamic Activity!", font=("Arial", 14, "bold"), padx=10, pady=5)
    label1.pack()

    label2 = tk.Label(window, text=f"Watch the {num_balls} balls!", font=("Arial", 10), padx=10, pady=2)
    label2.pack()

    text_area = tk.Text(window, height=2, width=40, wrap=tk.WORD, bg="lightgray")
    text_area.insert(tk.END, "This window is performing continuous animations...\n")
    text_area.pack(pady=5)
    text_area.config(state=tk.DISABLED)

    # Canvas for the simulated 3D ball animation
    canvas_width = window_width - 20 # Adjust for padding
    canvas_height = 150
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="darkblue", bd=2, relief="sunken")
    canvas.pack(pady=5)
    window.canvas = canvas # Store canvas on window for easy access in animation function

    def animate_ball():
        """
        Animates simulated 3D balls on the canvas.
        Each ball moves, bounces off edges, and its size pulses.
        """
        if not window.winfo_exists():
            return # Stop animation if window is closed

        canvas.delete("all")

        # Iterate through each ball's data and update/draw it
        for ball_data in window.balls_data:
            # Update ball position
            ball_data['x'] += ball_data['dx']
            ball_data['y'] += ball_data['dy']

            # Bounce off canvas edges
            if ball_data['x'] + ball_data['radius'] > canvas_width or ball_data['x'] - ball_data['radius'] < 0:
                ball_data['dx'] *= -1
            if ball_data['y'] + ball_data['radius'] > canvas_height or ball_data['y'] - ball_data['radius'] < 0:
                ball_data['dy'] *= -1

            # Update ball radius for "3D" pulsing effect
            ball_data['radius'] += ball_data['radius_direction'] * 0.5 # Smaller step for smoother pulse
            if ball_data['radius'] >= 60: # Max radius
                ball_data['radius_direction'] = -1
            elif ball_data['radius'] <= 40: # Min radius
                ball_data['radius_direction'] = 1

            # Calculate a color based on radius to simulate depth/intensity
            # Lighter when larger (closer), darker when smaller (further)
            # Add unique color offset for each ball
            intensity = int(255 * (ball_data['radius'] - 40) / 20)
            color_val = max(0, min(255, intensity + ball_data['color_offset']))
            ball_color = f"#FF{color_val:02x}{color_val:02x}" # Red base, green/blue vary

            # Draw the ball (oval)
            canvas.create_oval(
                ball_data['x'] - ball_data['radius'],
                ball_data['y'] - ball_data['radius'],
                ball_data['x'] + ball_data['radius'],
                ball_data['y'] + ball_data['radius'],
                fill=ball_color,
                outline="white",
                width=2
            )

        window.after(20, animate_ball) # Update ball animation every 20 milliseconds

    def move_window_around():
        """
        Moves the window around the screen, bouncing off the screen edges.
        """
        if not window.winfo_exists():
            return # Stop movement if window is closed

        current_geometry = window.geometry().split('+')
        current_x = int(current_geometry[1])
        current_y = int(current_geometry[2])

        new_x = current_x + window.x_dir
        new_y = current_y + window.y_dir

        # Reverse direction if hitting screen edges
        if new_x + window_width > screen_width or new_x < 0:
            window.x_dir *= -1
            new_x = current_x + window.x_dir # Re-calculate new_x after bounce
        if new_y + window_height > screen_height or new_y < 0:
            window.y_dir *= -1
            new_y = current_y + window.y_dir # Re-calculate new_y after bounce

        window.geometry(f"{window_width}x{window_height}+{new_x}+{new_y}")
        window.after(50, move_window_around) # Update window position every 50 milliseconds

    # Start the animations and movement for this window
    animate_ball()
    move_window_around()

    # Add a close button
    close_button = tk.Button(window, text="Close This Dynamic Window", command=window.destroy, bg="red", fg="white")
    close_button.pack(pady=5)

    # When a window is closed, remove it from the active_windows list
    window.protocol("WM_DELETE_WINDOW", lambda: on_window_close(window))
    active_windows.append(window) # Add to list of active windows

def on_window_close(window):
    """Handles cleanup when a window is closed."""
    window.destroy()
    if window in active_windows:
        active_windows.remove(window)

def create_batch_of_windows(root_instance):
    """
    Creates a batch of 20 new windows almost instantly, and then schedules
    the next batch to be created after 1 second.
    """
    global batch_counter # Access the global counter
    if root_instance.winfo_exists(): # Only create if the root is still active
        batch_counter += 1
        print(f"Opening batch {batch_counter}: 20 windows...")
        for _ in range(20): # Open 20 windows almost instantly
            try:
                create_window()
                # This line helps Tkinter process the new window faster,
                # potentially making the batch appear more synchronously.
                root_instance.update_idletasks()
            except Exception as e:
                print(f"Error creating window in batch {batch_counter}: {e}")
                # If an error occurs, it's safer to break and not continue this batch
                # to prevent a cascade of errors or a complete freeze.
                break
        # Schedule the next batch to open in 1000 milliseconds (1 second)
        root_instance.after(1000, lambda: create_batch_of_windows(root_instance))
    else:
        print("Root window closed or does not exist, stopping new window batch creation.")

def spam_windows_continuously():
    """
    Continuously spams Tkinter windows by opening batches of 20 windows every second.
    Windows do not auto-close, move around, and each displays simulated 3D ball animations.
    """
    root = tk.Tk()
    root.withdraw() # Hide the main root window

    print("Starting continuous spam of dynamic, intensive Tkinter windows (batches of 20 windows/second, no auto-close).")
    print("Windows will move around and display a simulated 3D ball animation.")
    print("Close the terminal or all individual windows to stop the program.")

    # Start the first batch creation, which will then schedule subsequent batches
    create_batch_of_windows(root)

    # Start the Tkinter event loop. This keeps the program running and processes all GUI events.
    try:
        root.mainloop()
    except Exception as e:
        print(f"An unexpected error occurred in the main Tkinter loop: {e}")
    finally:
        print("Main Tkinter loop terminated. All windows should be closed.")


if __name__ == "__main__":
    spam_windows_continuously()
