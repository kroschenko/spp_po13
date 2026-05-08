"""
Moving text strings across the screen.
Each string moves in random direction; speed and pause can be controlled.
"""

import os
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageGrab

class MovingTextApp:
    """Main application for moving text strings."""

    def __init__(self, master):
        self.root = master
        self.root.title("Moving Text Strings")
        self.root.geometry("800x600")

        self.texts = ["Hello", "World", "Python", "Tkinter", "Animation",
                      "Dragons", "Random", "Speed", "Pause", "Screenshot"]
        self.speed = 10
        self.running = True
        self.strings = []

        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(control_frame, text="Start", command=self.start_animation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Pause", command=self.pause_animation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Screenshot", command=self.take_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Add Random String", command=self.add_random_string).pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Speed (ms):").pack(side=tk.LEFT, padx=(20, 5))
        self.speed_var = tk.IntVar(value=self.speed)
        speed_spin = ttk.Spinbox(control_frame, from_=1, to=100, textvariable=self.speed_var,
                                 width=5, command=self.update_speed)
        speed_spin.pack(side=tk.LEFT)

        self.create_initial_strings()
        self.animate()

    def create_initial_strings(self):
        for _ in range(5):
            self.add_random_string()

    def add_random_string(self):
        text = random.choice(self.texts)
        x = random.randint(50, self.canvas.winfo_width() - 50) if self.canvas.winfo_width() > 100 else 100
        y = random.randint(50, self.canvas.winfo_height() - 50) if self.canvas.winfo_height() > 100 else 100
        dx = random.choice([-2, -1, 1, 2])
        dy = random.choice([-2, -1, 0, 1, 2])
        if dx == 0 and dy == 0:
            dy = 1
        color = random.choice(['red', 'blue', 'green', 'purple', 'orange', 'black'])
        font = ('Arial', random.randint(12, 24))
        item_id = self.canvas.create_text(x, y, text=text, fill=color, font=font)
        self.strings.append({
            'id': item_id,
            'dx': dx,
            'dy': dy,
            'text': text,
            'color': color,
            'font': font
        })

    def update_speed(self):
        self.speed = self.speed_var.get()

    def start_animation(self):
        self.running = True

    def pause_animation(self):
        self.running = False

    def take_screenshot(self):
        try:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            img = ImageGrab.grab(bbox=(x, y, x1, y1))
            counter = 1
            while os.path.exists(f"screenshot_{counter}.png"):
                counter += 1
            filename = f"screenshot_{counter}.png"
            img.save(filename)
            messagebox.showinfo("Screenshot", f"Saved as {filename}")
        except (OSError, IOError, AttributeError) as e:
            messagebox.showerror("Error", f"Could not take screenshot: {e}")

    def animate(self):
        if self.running:
            for obj in self.strings:
                self.canvas.move(obj['id'], obj['dx'], obj['dy'])
                pos = self.canvas.coords(obj['id'])
                if pos:
                    x, y = pos[0], pos[1]
                    if x < 10 or x > self.canvas.winfo_width() - 10:
                        obj['dx'] = -obj['dx']
                    if y < 10 or y > self.canvas.winfo_height() - 10:
                        obj['dy'] = -obj['dy']
        self.root.after(self.speed, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = MovingTextApp(root)
    root.mainloop()
