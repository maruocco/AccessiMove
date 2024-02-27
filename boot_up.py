# Michael Ruocco, boot_up.py: Class displays boot up logo when main app is launched
import tkinter as tk
from PIL import Image, ImageTk


class BootUp:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Create a borderless window
        self.root.attributes("-transparentcolor", "white")  # Set white color as transparent
        self.root.attributes("-topmost", True)  # Keep the window on top

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        image = Image.open(image_path)
        image_width, image_height = image.size
        x = (screen_width - image_width) // 2
        y = (screen_height - image_height) // 2
        self.root.geometry("+{}+{}".format(x, y))

        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        label = tk.Label(self.root, image=photo, bg='white')
        label.photo = photo  # Keep a reference to avoid garbage collection
        label.pack(expand=True, fill=tk.BOTH)

        self.done_displaying = False

    def display_image(self):
        self.root.after(5000, self.set_done_displaying)
        self.root.mainloop()

    def set_done_displaying(self):
        self.done_displaying = True
        self.root.destroy()
