"""Rotating triangle module."""

# pylint: disable=too-many-arguments, too-many-instance-attributes
# pylint: disable=too-few-public-methods, duplicate-code
# pylint: disable=too-many-positional-arguments

import tkinter as tk
from tkinter import ttk
import math
import time
from PIL import ImageGrab


class Triangle:
    """Triangle class with rotation around center of mass."""

    def __init__(self, p1, p2, p3):
        self.vertices = [p1, p2, p3]
        self.angle = 0
        self._update_center()

    def _update_center(self):
        """Calculate center of mass (centroid)."""
        cx = sum(v[0] for v in self.vertices) / 3
        cy = sum(v[1] for v in self.vertices) / 3
        self.center = (cx, cy)

    def rotate(self, degrees):
        """Rotate triangle by given degrees."""
        self.angle += degrees
        rad = math.radians(degrees)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        cx, cy = self.center

        rotated = []
        for x, y in self.vertices:
            dx = x - cx
            dy = y - cy
            new_x = cx + dx * cos_a - dy * sin_a
            new_y = cy + dx * sin_a + dy * cos_a
            rotated.append((new_x, new_y))
        self.vertices = rotated

    def get_vertices(self):
        """Get current vertices."""
        return self.vertices


class TriangleApp:
    """Main application class."""

    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Вращающийся треугольник")
        self.parent.geometry("800x700")
        self.parent.configure(bg="#2c3e50")

        self.is_running = True
        self.after_id = None
        self.triangle = None

        self._create_controls()
        self._create_canvas()
        self._init_triangle()
        self._animate()

    def _create_controls(self):
        """Create control panel."""
        control_frame = tk.Frame(self.parent, bg="#34495e")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(
            control_frame,
            text="Скорость вращения:",
            bg="#34495e",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=10)

        self.speed_var = tk.DoubleVar(value=2.0)
        tk.Scale(
            control_frame,
            from_=0.5,
            to=10.0,
            resolution=0.5,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            bg="#34495e",
            fg="white",
            length=200
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            control_frame,
            text="Цвет:",
            bg="#34495e",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=10)

        self.color_var = tk.StringVar(value="#e74c3c")
        colors = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]
        color_menu = ttk.Combobox(
            control_frame,
            textvariable=self.color_var,
            values=colors,
            state="readonly",
            width=10
        )
        color_menu.pack(side=tk.LEFT, padx=10)
        color_menu.bind("<<ComboboxSelected>>", self._update_color)

        self.pause_btn = tk.Button(
            control_frame,
            text="⏸ Пауза",
            command=self._toggle_pause,
            bg="#e74c3c",
            fg="white",
            width=10
        )
        self.pause_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(
            control_frame,
            text="📸 Скриншот",
            command=self._take_screenshot,
            bg="#3498db",
            fg="white",
            width=12
        ).pack(side=tk.LEFT, padx=10)

        self.info_label = tk.Label(
            control_frame,
            text="Треугольник вращается",
            bg="#34495e",
            fg="white",
            font=("Arial", 10)
        )
        self.info_label.pack(side=tk.RIGHT, padx=20)

    def _create_canvas(self):
        """Create drawing canvas."""
        canvas_frame = tk.Frame(self.parent, bg="#2c3e50")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="#ecf0f1",
            highlightthickness=2,
            highlightbackground="#bdc3c7"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self._on_resize)

    def _init_triangle(self):
        """Create initial triangle."""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 100 or h < 100:
            w, h = 700, 500

        size = min(w, h) * 0.4
        cx, cy = w // 2, h // 2

        self.triangle = Triangle(
            (cx - size * 0.5, cy - size * 0.4),
            (cx + size * 0.5, cy - size * 0.2),
            (cx, cy + size * 0.6)
        )

    def _draw_triangle(self):
        """Draw triangle on canvas."""
        self.canvas.delete("all")
        vertices = self.triangle.get_vertices()
        flat = []
        for vert in vertices:
            flat.extend([vert[0], vert[1]])

        self.canvas.create_polygon(
            flat,
            fill=self.color_var.get(),
            outline="#2c3e50",
            width=3,
            tags="triangle"
        )

        cx, cy = self.triangle.center
        r = 5
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#e74c3c",
            outline="#c0392b",
            width=2
        )

    def _animate(self):
        """Animation loop."""
        if not self.is_running:
            self.after_id = None
            return

        speed = self.speed_var.get()
        self.triangle.rotate(speed)
        self._draw_triangle()
        self.info_label.config(text=f"Угол поворота: {int(self.triangle.angle % 360)}°")

        delay = int(50 / max(speed, 0.5))
        self.after_id = self.parent.after(delay, self._animate)

    def _toggle_pause(self):
        """Pause/resume animation."""
        self.is_running = not self.is_running
        if self.is_running:
            self.pause_btn.config(text="⏸ Пауза", bg="#e74c3c")
            self._animate()
        else:
            self.pause_btn.config(text="▶ Старт", bg="#2ecc71")
            if self.after_id:
                self.parent.after_cancel(self.after_id)
                self.after_id = None

    def _update_color(self, _event=None):
        """Update triangle color."""
        self._draw_triangle()

    def _on_resize(self, _event=None):
        """Handle canvas resize."""
        self._init_triangle()
        self._draw_triangle()

    def _take_screenshot(self):
        """Save screenshot."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_triangle_{timestamp}.png"

        x = self.parent.winfo_rootx() + self.canvas.winfo_x()
        y = self.parent.winfo_rooty() + self.canvas.winfo_y()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
        img.save(filename)
        self.info_label.config(text=f"Скриншот сохранён: {filename}")
        self.parent.after(2000, lambda: self.info_label.config(
            text="Треугольник вращается"
        ))

    def on_closing(self):
        """Handle window closing."""
        if self.after_id:
            self.parent.after_cancel(self.after_id)
        self.parent.destroy()


if __name__ == "__main__":
    ROOT = tk.Tk()
    APP = TriangleApp(ROOT)
    ROOT.protocol("WM_DELETE_WINDOW", APP.on_closing)
    ROOT.mainloop()
