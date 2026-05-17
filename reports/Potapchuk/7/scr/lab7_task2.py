import tkinter as tk
import os
from PIL import ImageGrab


class DragonFractal:
    def __init__(self, root):
        self.root = root
        self.root.title("Задание 2")
        self.menu = tk.Frame(root)
        self.menu.pack(pady=10)
        tk.Label(self.menu, text="Глубина:").pack(side=tk.LEFT)
        self.depth_spn = tk.Spinbox(self.menu, from_=1, to=14, width=5)
        self.depth_spn.pack(side=tk.LEFT, padx=5)
        self.depth_spn.delete(0, "end")
        self.depth_spn.insert(0, "1")
        tk.Button(self.menu, text="Отрисовать", command=self.start_draw).pack(side=tk.LEFT)
        tk.Button(self.menu, text="Скриншот", command=self.save_img).pack(side=tk.LEFT, padx=5)
        self.canvas = tk.Canvas(root, width=700, height=600, bg="#1e1e1e")
        self.canvas.pack(padx=10, pady=10)

    # pylint: disable=too-many-positional-arguments
    def draw_dragon(self, x1, y1, x2, y2, k):
        """Рекурсивное построение фрактала."""
        if k == 0:
            self.canvas.create_line(x1, y1, x2, y2, fill="#00FF7F", width=1)
        else:
            xn = (x1 + x2) / 2 + (y2 - y1) / 2
            yn = (y1 + y2) / 2 - (x2 - x1) / 2
            self.draw_dragon(x2, y2, xn, yn, k - 1)
            self.draw_dragon(x1, y1, xn, yn, k - 1)

    def start_draw(self):
        self.canvas.delete("all")
        d = int(self.depth_spn.get())
        self.draw_dragon(200, 200, 500, 450, d)

    def save_img(self):
        self.root.update()
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        path = os.path.join(os.getcwd(), "dragon_fractal.png")
        ImageGrab.grab(bbox=(x, y, x + w, y + h)).save(path)
        print(f"Фрактал сохранен: {path}")


if __name__ == "__main__":
    base = tk.Tk()
    app = DragonFractal(base)
    base.mainloop()
