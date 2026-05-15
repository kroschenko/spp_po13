"""ЛР7 (вариант 3): простая версия GUI."""

import math
from datetime import datetime
import tkinter as tk
from tkinter import ttk


def rotate_point(x, y, angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return x * c - y * s, x * s + y * c


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ЛР7 вариант 3")
        self.root.geometry("980x620")

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        self.make_tab_rotation()
        self.make_tab_fractal()

    def make_tab_rotation(self):
        self.tab1 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Вращение")

        self.canvas1 = tk.Canvas(self.tab1, bg="white")
        self.canvas1.pack(fill="both", expand=True, padx=8, pady=8)

        controls = ttk.Frame(self.tab1)
        controls.pack(fill="x", padx=8, pady=4)

        self.speed = tk.DoubleVar(value=2.5)
        self.paused = tk.BooleanVar(value=False)

        ttk.Label(controls, text="Скорость:").pack(side="left")
        ttk.Scale(controls, from_=0.5, to=8, variable=self.speed, orient="horizontal").pack(
            side="left", fill="x", expand=True, padx=8
        )
        ttk.Checkbutton(controls, text="Пауза", variable=self.paused).pack(side="left", padx=8)
        ttk.Button(controls, text="Скриншот", command=self.save1).pack(side="left")

        self.base = [(-120, -80), (130, -60), (90, 100), (-130, 70)]
        self.angle = 0.0
        self.animate()

    def animate(self):
        if not self.paused.get():
            self.angle += self.speed.get() * math.pi / 180

        w = self.canvas1.winfo_width()
        h = self.canvas1.winfo_height()
        cx, cy = w / 2, h / 2

        pts = []
        for x, y in self.base:
            rx, ry = rotate_point(x, y, self.angle)
            pts.extend([cx + rx, cy + ry])

        self.canvas1.delete("all")
        self.canvas1.create_polygon(pts, outline="black", fill="#8ec9ff", width=2)
        self.canvas1.create_text(10, 10, text="Четырехугольник вращается", anchor="nw")
        self.root.after(30, self.animate)

    def make_tab_fractal(self):
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab2, text="Серпинский")

        self.canvas2 = tk.Canvas(self.tab2, bg="white")
        self.canvas2.pack(fill="both", expand=True, padx=8, pady=8)

        controls = ttk.Frame(self.tab2)
        controls.pack(fill="x", padx=8, pady=4)

        self.depth = tk.IntVar(value=5)
        ttk.Label(controls, text="Глубина:").pack(side="left")
        ttk.Spinbox(controls, from_=0, to=8, textvariable=self.depth, width=6).pack(side="left", padx=8)
        ttk.Button(controls, text="Построить", command=self.draw_fractal).pack(side="left")
        ttk.Button(controls, text="Скриншот", command=self.save2).pack(side="left", padx=8)

        self.canvas2.bind("<Configure>", lambda _e: self.draw_fractal())
        self.draw_fractal()

    def tri(self, p1, p2, p3, d):
        if d == 0:
            self.canvas2.create_polygon([p1, p2, p3], outline="navy", fill="#dbe9ff")
            return
        a = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        b = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        c = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)
        self.tri(p1, a, c, d - 1)
        self.tri(a, p2, b, d - 1)
        self.tri(c, b, p3, d - 1)

    def draw_fractal(self):
        self.canvas2.delete("all")
        w = self.canvas2.winfo_width()
        h = self.canvas2.winfo_height()
        size = min(w, h) * 0.8
        top = (w / 2, h / 2 - size / 2)
        left = (w / 2 - size / 2, h / 2 + size / 3)
        right = (w / 2 + size / 2, h / 2 + size / 3)
        self.tri(top, left, right, max(0, self.depth.get()))

    def save1(self):
        name = f"lr7_quad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ps"
        self.canvas1.postscript(file=name, colormode="color")

    def save2(self):
        name = f"lr7_sierpinski_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ps"
        self.canvas2.postscript(file=name, colormode="color")


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
