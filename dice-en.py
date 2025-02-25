# Import necessary modules
import tkinter as tk                               # Tkinter for GUI
from tkinter import Frame, Label, Button, Entry, messagebox, colorchooser  # Important Tkinter widgets and functions
import random                                      # Random number generator for rolling dice
import math                                        # Mathematical functions (e.g., ceil)
import matplotlib.pyplot as plt                    # Plotting library for graphical dice display
import numpy as np                                 # Numpy for potential calculations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Embed Matplotlib figures into Tkinter

# Try to import the module that provides a custom integer entry widget (IntEntry)
try:
    from number_entry import IntEntry
except ImportError:
    # Display an error message and exit if the module is missing
    messagebox.showerror("Error", "number_entry module is missing.")
    exit()

# Global variables used later for calculating cell dimensions in the results area
cell_width = 0
cell_height = 0
# Factors that indicate what portion of the cell's width and height is used for drawing dice
dice_area_width_factor = 0.9   # 90% of the cell width is used
dice_area_height_factor = 0.5  # 50% of the cell height is used

def draw_dice_face(ax, number, dice_color, text_color, use_dots=False):
    """
    Draws a single dice face on the given Matplotlib axis (ax).

    Parameters:
      ax         - Matplotlib axis to draw on
      number     - The rolled number
      dice_color - Background color of the dice
      text_color - Color for the number or the pips (dots)
      use_dots   - If True, draws a pip pattern (typical dice pips) instead of a number
    """
    # Clear the current axis content
    ax.clear()
    # Remove axis ticks for a clean look
    ax.set_xticks([])
    ax.set_yticks([])
    # Set fixed axis limits
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    # Set the background color of the dice face
    ax.set_facecolor(dice_color)

    # If pip display is activated (for dice with 6 or fewer sides)
    if use_dots:
        # Define pip positions for the typical dice faces
        pip_positions = {
            1: [(0.25, 0.25)],  # One pip in the center
            2: [(0.1, 0.4), (0.4, 0.1)],  # Two pips diagonally placed
            3: [(0.1, 0.4), (0.25, 0.25), (0.4, 0.1)],  # Three pips with one in the center
            4: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1)],  # Four pips in the corners
            5: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.1), (0.4, 0.1), (0.25, 0.25)],  # Four corners plus a center pip
            6: [(0.1, 0.4), (0.4, 0.4), (0.1, 0.25), (0.4, 0.25), (0.1, 0.1), (0.4, 0.1)]  # Six pips in two columns
        }
        # Retrieve the pip positions for the rolled number; default to a single center pip if undefined
        dots = pip_positions.get(number, [(0.25, 0.25)])
        # Draw each pip as a small circle on the axis
        for (x, y) in dots:
            circle = plt.Circle((x, y), 0.04, color=text_color)
            ax.add_artist(circle)
    else:
        # If not using pips, simply display the number in the center of the dice face
        ax.text(0.25, 0.25, str(number), fontsize=16, ha='center', va='center',
                fontweight='bold', color=text_color)

def roll_single_set(result_frame, dice_count, dice_sides, set_name, dice_color, number_color):
    """
    Rolls a single set of dice and displays the results graphically.

    Parameters:
      result_frame - The Tkinter frame where the dice images will be shown
      dice_count   - Entry widget for the number of dice to roll
      dice_sides   - Entry widget for the number of sides on the dice
      set_name     - Name of the set (used for labeling)
      dice_color   - Background color of the dice
      number_color - Color of the displayed number or pips
    """
    # Remove any previous widgets from the result frame for a clean start
    for widget in result_frame.winfo_children():
        widget.destroy()
    
    try:
        # Retrieve the number of sides and the dice count from the entry widgets
        sides_val = dice_sides.get()
        count_val = dice_count.get()
        # Validate that the entered values are within allowed ranges (Sides: 2-50, Dice Count: 1-12)
        if not (2 <= sides_val <= 50) or not (1 <= count_val <= 12):
            raise ValueError
        # Generate a list of random rolls based on the given number of dice and sides
        rolls = [random.randint(1, sides_val) for _ in range(count_val)]
    except ValueError:
        # Display an error message if the input values are invalid
        messagebox.showerror("Input Error", "Please enter valid values for sides (2-50) and dice count (1-12).")
        return

    # Determine how many dice to display per row (maximum of 6 per row)
    dice_cols = min(6, count_val)
    # Calculate the required number of rows based on the total dice count
    dice_rows = math.ceil(count_val / 6)

    # Calculate the size of each dice in pixels based on the current window size and defined factors
    die_size_pixels = min((cell_width * dice_area_width_factor) / dice_cols,
                          (cell_height * dice_area_height_factor) / dice_rows)
    # Convert pixel size to inches (assuming 100 dpi: 1 inch = 100 pixels)
    fig_width = (die_size_pixels * dice_cols) / 100
    fig_height = (die_size_pixels * dice_rows) / 100

    # Create a Matplotlib figure with a grid of subplots for the dice
    fig, axes = plt.subplots(dice_rows, dice_cols, figsize=(fig_width, fig_height), dpi=100)
    # Flatten the axes to a single list regardless of grid configuration
    if dice_rows * dice_cols == 1:
        axes = [axes]
    elif dice_rows == 1 or dice_cols == 1:
        axes = list(axes)
    else:
        axes = [ax for row in axes for ax in row]

    # Decide whether to use pip display based on the number of sides (use pips if 6 or less)
    use_dots = (sides_val <= 6)
    # Draw each dice face on the corresponding axis
    for ax, roll in zip(axes, rolls):
        draw_dice_face(ax, roll, dice_color, number_color, use_dots=use_dots)
    # Hide any extra axes if fewer dice were rolled than the available subplots
    for ax in axes[len(rolls):]:
        ax.set_visible(False)
    
    # Embed the Matplotlib figure into the result frame in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=result_frame)
    canvas.get_tk_widget().pack(pady=5)
    canvas.draw()
    
    # If more than one dice was rolled, display the total result sum below the dice
    if count_val > 1:
        total = sum(rolls)
        Label(result_frame, text=f"Total: {total}", font=("Arial", 12, "bold")).pack(pady=5)

def confirm_sets():
    """
    Reads the number of sets entered by the user, validates it,
    creates a configuration field for each set, and stores the sets globally.
    """
    try:
        # Retrieve the number of sets from the entry widget
        num_sets = enter_set.get()
        # Validate that the number of sets is within the allowed range (1-12)
        if not (1 <= num_sets <= 12):
            raise ValueError
    except:
        # Show an error message if the input is invalid
        messagebox.showerror("Error", "Please enter a valid number of sets (1-12).")
        return

    # Reinitialize the global list of sets
    global sets
    sets = []
    # Clear any previous set configurations from the grid frame
    for widget in grid_frame.winfo_children():
        widget.destroy()
    
    # Create a configuration frame for each set
    # Sets are arranged in a grid with a maximum of 4 rows per column
    for i in range(num_sets):
        # Create a frame for the set with a border and padding
        set_frame = Frame(grid_frame, bd=1, relief="groove", padx=5, pady=5)
        # Position the frame in the grid (row and column indices are calculated dynamically)
        set_frame.grid(row=i % 4, column=i // 4, padx=10, pady=10, sticky="nsew")
        
        # Entry for the set name
        Label(set_frame, text=f"Set {i+1} Name:").grid(row=0, column=0, sticky="w")
        set_name = Entry(set_frame, width=15)
        set_name.grid(row=0, column=1, padx=5, pady=2)
        
        # Entry for the dice count in this set
        Label(set_frame, text="Dice Count (max. 12):").grid(row=1, column=0, sticky="w")
        dice_count = IntEntry(set_frame, width=5, lower_bound=1, upper_bound=12)
        dice_count.grid(row=1, column=1, padx=5, pady=2)
        
        # Entry for the number of sides per dice
        Label(set_frame, text="Dice Sides (max. 50):").grid(row=2, column=0, sticky="w")
        dice_sides = IntEntry(set_frame, width=5, lower_bound=2, upper_bound=50)
        dice_sides.grid(row=2, column=1, padx=5, pady=2)
        
        # Color selection for the dice face
        Label(set_frame, text="Dice Color:").grid(row=3, column=0, sticky="w")
        dice_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="white")
        dice_color_label.grid(row=3, column=1, padx=5, pady=2)
        Button(set_frame, text="Choose", 
               command=lambda lbl=dice_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "white")
        ).grid(row=3, column=2, padx=5, pady=2)
        
        # Color selection for the number or pip color
        Label(set_frame, text="Number Color:").grid(row=4, column=0, sticky="w")
        text_color_label = Label(set_frame, text=" ", width=8, relief="solid", bg="black")
        text_color_label.grid(row=4, column=1, padx=5, pady=2)
        Button(set_frame, text="Choose", 
               command=lambda lbl=text_color_label: lbl.config(bg=colorchooser.askcolor()[1] or "black")
        ).grid(row=4, column=2, padx=5, pady=2)
        
        # Add this set configuration to the global list
        sets.append((set_name, dice_count, dice_sides, dice_color_label, text_color_label))

def show_dice_results():
    """
    Displays the dice roll results by hiding the settings view and showing a result frame for each set.
    """
    # Hide the settings frame
    settings_frame.pack_forget()
    # Clear any previous result widgets
    for widget in results_menu.winfo_children():
        widget.destroy()
    
    # Automatically adjust the window size based on screen dimensions and the number of sets
    n_sets = len(sets)
    # Determine the number of rows: if there are 3 or more sets, use 3 rows; otherwise, use the number of sets
    n_rows = 3 if n_sets >= 3 else n_sets
    # Determine the number of columns needed (rounding up)
    n_columns = math.ceil(n_sets / 3)
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Define the desired window dimensions with a small margin
    desired_width = screen_width - 50
    desired_height = screen_height - 100
    global cell_width, cell_height
    cell_width = desired_width / n_columns
    cell_height = desired_height / n_rows
    # Set the window size
    root.geometry(f"{desired_width}x{desired_height}")
    
    # Create a header frame with a button to return to settings
    header_frame = Frame(results_menu)
    header_frame.pack(side="top", fill="x", pady=5)
    Button(header_frame, text="Back to Settings", command=show_settings).pack(padx=5, pady=5)
    
    # Create a content frame where each set's results will be displayed
    content_frame = Frame(results_menu)
    content_frame.pack(fill="both", expand=True)
    
    # For each set, create its own frame and display the dice
    for i, (set_name, dice_count, dice_sides, dice_color_label, text_color_label) in enumerate(sets):
        # Create a fixed-size frame for the set
        set_frame = Frame(content_frame, bd=1, relief="groove", width=int(cell_width), height=int(cell_height))
        set_frame.grid_propagate(False)  # Prevent the frame from resizing based on its content
        set_frame.grid(row=i % 3, column=i // 3, padx=10, pady=10, sticky="nsew")
        
        # Within the set frame, create a result frame where the dice will be drawn
        result_frame = Frame(set_frame)
        result_frame.pack(fill="both", expand=True)
        # Create a button that triggers rolling for this set
        Button(set_frame, text=f"{set_name.get()} - Roll Dice", 
               command=lambda rf=result_frame, dc=dice_count, ds=dice_sides, sn=set_name, 
                              dc_lbl=dice_color_label, tc_lbl=text_color_label: roll_single_set(
                                  rf, dc, ds, sn.get(), dc_lbl["bg"], tc_lbl["bg"])
        ).pack(side="bottom", pady=2)
    
    # Display the results frame
    results_menu.pack(fill="both", expand=True)

def show_settings():
    """
    Shows the settings view by hiding the results view.
    """
    results_menu.pack_forget()
    settings_frame.pack(fill="both", expand=True)

# Create the main application window
root = tk.Tk()
# Set a default font for all widgets
root.option_add("*Font", "Arial 12")
# Set the window title
root.title("Dice Roller with Adaptive Sizes")

# Global list that will store each set's configuration
sets = []

# Create the settings frame where the user enters the number of sets and their parameters
settings_frame = Frame(root)
settings_frame.pack(fill="both", expand=True)

# Top section of the settings frame: entry for the number of sets to roll
top_frame = Frame(settings_frame)
top_frame.pack(side="top", fill="x", pady=5)

# Label and entry for the number of sets (1-12)
Label(top_frame, text="How many sets do you want to roll? (1-12)").grid(row=0, column=0, padx=5)
enter_set = IntEntry(top_frame, width=5, lower_bound=1, upper_bound=12)
enter_set.grid(row=0, column=1, padx=5)
# Button to proceed to set configuration
Button(top_frame, text="Next", command=confirm_sets).grid(row=0, column=2, padx=5)
# Button to immediately show the dice results (after configuring the sets)
Button(top_frame, text="Confirm Settings", command=show_dice_results).grid(row=0, column=3, padx=5)

# Frame to hold the configuration of each set
grid_frame = Frame(settings_frame)
grid_frame.pack(fill="both", expand=True)

# Frame that will later display the dice roll results
results_menu = Frame(root)

# Start the Tkinter main loop to run the GUI
root.mainloop()
