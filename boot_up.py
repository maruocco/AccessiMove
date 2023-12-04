# Michael Ruocco
# This class creates a splash screen when the program boots up and opens the settings menu after x amount of time.

import tkinter as tk
from tkinter import PhotoImage

# Create a splash screen window
splash = tk.Tk()
splash.title("")
splash.overrideredirect(True)
image = PhotoImage(file="Images/splash_screen.png")
splash.geometry(f"{image.width()}x{image.height()}")
splash_label = tk.Label(splash, image=image)
splash_label.pack()
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width - image.width()) // 2
y = (screen_height - image.height()) // 2
splash.geometry(f"{image.width()}x{image.height()}+{x}+{y}")


# Function to close the splash screen and open the main window
def open_main_window():
    # Close splash screen
    splash.destroy()

    # Create main menu
    root = tk.Tk()
    root.title("AccessiMove")
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")


    # Run main menu
    root.mainloop()


# delay for splash screen
splash.after(3000, open_main_window())

# Run splash screen
splash.mainloop()
