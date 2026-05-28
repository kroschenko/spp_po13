"""Sierpinski carpet fractal module."""

# pylint: disable=too-many-arguments, too-many-instance-attributes
# pylint: disable=too-few-public-methods, duplicate-code
# pylint: disable=too-many-positional-arguments

import tkinter as tk
from tkinter import ttk
import time
from PIL import ImageGrab


class SierpinskiCarpet:
    """Sierpinski carpet fractal generator."""

    def __init__(self, size, depth):
        self.size = size
        self.depth = depth

    def generate(self):
        """Generate fractal pattern."""
        pixels = [[1] * self.size for _ in range(self.size)]
        self._fill(pixels, 0, 0, self.size, self.depth)
        return pixels

    def _fill(self, pixels, x, y, cur_size, depth):
        """Recursively fill holes."""
        if depth == 0 or cur_size < 3:
            return

        new_size = cur_size // 3
        if new_size == 0:
            return

        cx = x + new_size
        cy = y + new_size
        for i in range(cy, cy + new_size):
            for j in range(cx, cx + new_size):
                if 0 <= i < self.size and 0 <= j < self.size:
                    pixels[i][j] = 0

        for row in range(3):
            for col in range(3):
                if row == 1 and col == 1:
                    continue
                self._fill(
                    pixels,
                    x + col * new_size,
                    y + row * new_size,
                    new_size,
                    depth - 1
                )


class CarpetApp:
    """Main application class."""

    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Ковёр Серпинского")
        self.parent.geometry("900x800")
        self.parent.configure(bg="#2c3e50")

        self.depth = 3
        self.size = 600
        self.after_id = None
        self.is_animating = False

        self._create_controls()
        self._create_canvas()
        self._draw_fractal()

    def _create_controls(self):
        """Create control panel."""
        control_frame = tk.Frame(self.parent, bg="#34495e")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        tk.Label(
            control_frame,
            text="Глубина рекурсии:",
            bg="#34495e",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=10)

        self.depth_var = tk.IntVar(value=self.depth)
        tk.Scale(
            control_frame,
            from_=1,
            to=5,
            orient=tk.HORIZONTAL,
            variable=self.depth_var,
            bg="#34495e",
            fg="white",
            length=150
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            control_frame,
            text="Цвет:",
            bg="#34495e",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=10)

        self.color_var = tk.StringVar(value="#2ecc71")
        colors = ["#2ecc71", "#3498db", "#e74c3c", "#f1c40f", "#9b59b6", "#1abc9c"]
        color_menu = ttk.Combobox(
            control_frame,
            textvariable=self.color_var,
            values=colors,
            state="readonly",
            width=10
        )
        color_menu.pack(side=tk.LEFT, padx=10)
        color_menu.bind("<<ComboboxSelected>>", self._redraw)

        tk.Label(
            control_frame,
            text="Фон:",
            bg="#34495e",
            fg="white",
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=10)

        self.bg_var = tk.StringVar(value="#ecf0f1")
        bg_colors = ["#ecf0f1", "#2c3e50", "#1a1a2e", "#16213e", "#0f3460"]
        bg_menu = ttk.Combobox(
            control_frame,
            textvariable=self.bg_var,
            values=bg_colors,
            state="readonly",
            width=10
        )
        bg_menu.pack(side=tk.LEFT, padx=10)
        bg_menu.bind("<<ComboboxSelected>>", self._redraw)

        self.animate_btn = tk.Button(
            control_frame,
            text="🎬 Анимация",
            command=self._toggle_animation,
            bg="#e74c3c",
            fg="white",
            width=12
        )
        self.animate_btn.pack(side=tk.LEFT, padx=10)

        tk.Button(
            control_frame,
            text="📸 Скриншот",
            command=self._take_screenshot,
            bg="#3498db",
            fg="white",
            width=12
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            control_frame,
            text="🔄 Перерисовать",
            command=self._redraw,
            bg="#9b59b6",
            fg="white",
            width=14
        ).pack(side=tk.LEFT, padx=10)

        self.info_label = tk.Label(
            control_frame,
            text=f"Глубина: {self.depth}",
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

    def _draw_fractal(self):
        """Draw fractal on canvas."""
        self.canvas.delete("all")

        depth = self.depth_var.get()
        self.info_label.config(text=f"Построение фрактала глубины {depth}...")
        self.parent.update()

        carpet = SierpinskiCarpet(self.size, depth)
        pixels = carpet.generate()

        self.info_label.config(text=f"Глубина: {depth}")
        self.parent.update()

        color = self.color_var.get()
        self.canvas.configure(bg=self.bg_var.get())

        for y in range(self.size):
            for x in range(self.size):
                if pixels[y][x] == 1:
                    self.canvas.create_rectangle(
                        x, y, x + 1, y + 1,
                        fill=color,
                        outline=color
                    )
        self.parent.update()

    def _redraw(self, _event=None):
        """Redraw fractal."""
        self._draw_fractal()

    def _animate_step(self, current_depth):
        """Animation step."""
        if not self.is_animating:
            return

        if current_depth > self.depth_var.get():
            self.is_animating = False
            self.animate_btn.config(text="🎬 Анимация", bg="#e74c3c")
            self.info_label.config(text="Анимация завершена")
            return

        self.depth_var.set(current_depth)
        self._draw_fractal()
        self.info_label.config(text=f"Анимация: глубина {current_depth}")

        self.after_id = self.parent.after(800, lambda: self._animate_step(current_depth + 1))

    def _toggle_animation(self):
        """Start/stop animation."""
        if self.is_animating:
            self.is_animating = False
            if self.after_id:
                self.parent.after_cancel(self.after_id)
            self.animate_btn.config(text="🎬 Анимация", bg="#e74c3c")
            self.info_label.config(text="Анимация остановлена")
        else:
            self.is_animating = True
            self.animate_btn.config(text="⏸ Стоп", bg="#c0392b")
            self._animate_step(1)

    def _take_screenshot(self):
        """Save screenshot."""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        depth = self.depth_var.get()
        filename = f"screenshot_carpet_depth_{depth}_{timestamp}.png"

        x = self.parent.winfo_rootx() + self.canvas.winfo_x()
        y = self.parent.winfo_rooty() + self.canvas.winfo_y()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if w > 10 and h > 10:
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            img.save(filename)
            self.info_label.config(text=f"Скриншот сохранён: {filename}")
            self.parent.after(2000, lambda: self.info_label.config(
                text=f"Глубина: {depth}"
            ))

    def on_closing(self):
        """Handle window closing."""
        if self.after_id:
            self.parent.after_cancel(self.after_id)
        self.parent.destroy()


if __name__ == "__main__":
    ROOT = tk.Tk()
    APP = CarpetApp(ROOT)
    ROOT.protocol("WM_DELETE_WINDOW", APP.on_closing)
    ROOT.mainloop()
