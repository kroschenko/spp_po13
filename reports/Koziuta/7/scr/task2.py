"""
Dragon Curve fractal drawing with adjustable recursion depth.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math

class DragonCurveApp:
    """Draw Dragon Curve fractal on Canvas."""

    def __init__(self, root):
        self.root = root
        self.root.title("Dragon Curve Fractal")
        self.root.geometry("900x700")

        # Parameters
        self.depth = 10
        self.scale = 5
        self.angle = 90  # turning angle in degrees

        # Canvas
        self.canvas = tk.Canvas(root, bg='white', width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Control frame
        control_frame = ttk.Frame(root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Depth (1-18):").pack(side=tk.LEFT, padx=5)
        self.depth_var = tk.IntVar(value=self.depth)
        depth_spin = ttk.Spinbox(control_frame, from_=1, to=18, textvariable=self.depth_var,
                                 width=5, command=self.redraw)
        depth_spin.pack(side=tk.LEFT, padx=5)

        ttk.Label(control_frame, text="Scale (pixels per step):").pack(side=tk.LEFT, padx=5)
        self.scale_var = tk.IntVar(value=self.scale)
        scale_spin = ttk.Spinbox(control_frame, from_=2, to=20, textvariable=self.scale_var,
                                 width=5, command=self.redraw)
        scale_spin.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Redraw", command=self.redraw).pack(side=tk.LEFT, padx=10)
        ttk.Button(control_frame, text="Save as EPS", command=self.save_eps).pack(side=tk.LEFT, padx=5)

        self.redraw()

    def generate_dragon_curve(self, depth):
        """
        Generate dragon curve instructions as a string of turns.
        Using the classic algorithm:
        Start with "R" (right turn). For each next iteration:
        new = old + "R" + reverse(flip(old))
        where flip changes L<->R.
        """
        if depth == 0:
            return ""
        seq = "R"
        for _ in range(depth - 1):
            flipped = seq[::-1].replace('L', 'x').replace('R', 'L').replace('x', 'R')
            seq = seq + "R" + flipped
        return seq

    def draw_curve(self, seq):
        """Draw the dragon curve on canvas given the turn sequence."""
        self.canvas.delete("all")
        if not seq:
            return

        scale = self.scale_var.get()
        x, y = self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2
        angle = 0  # current direction angle in degrees (0 = right)
        points = [(x, y)]

        for turn in seq:
            if turn == 'R':
                angle += self.angle
            else:  # 'L'
                angle -= self.angle
            # Move forward
            x += scale * math.cos(math.radians(angle))
            y += scale * math.sin(math.radians(angle))
            points.append((x, y))

        # Draw lines
        for i in range(len(points) - 1):
            self.canvas.create_line(points[i][0], points[i][1],
                                    points[i+1][0], points[i+1][1],
                                    fill='darkblue', width=2)

        # Optionally adjust scroll region
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def redraw(self):
        """Regenerate fractal with current depth and scale."""
        depth = self.depth_var.get()
        if depth < 1:
            depth = 1
        if depth > 18:
            depth = 18
        self.depth_var.set(depth)
        seq = self.generate_dragon_curve(depth)
        self.draw_curve(seq)

    def save_eps(self):
        """Save canvas content as EPS file."""
        try:
            self.canvas.postscript(file="dragon_curve.eps", colormode='color')
            messagebox.showinfo("Save", "Saved as dragon_curve.eps")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save EPS: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DragonCurveApp(root)
    root.mainloop()
