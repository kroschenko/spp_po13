import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from PIL import ImageGrab
import os
from datetime import datetime


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x:.1f}, {self.y:.1f})"


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def area(self):
        return abs(
            (
                self.p1.x * (self.p2.y - self.p3.y)
                + self.p2.x * (self.p3.y - self.p1.y)
                + self.p3.x * (self.p1.y - self.p2.y)
            )
            / 2.0
        )

    def is_point_inside(self, point):
        # Вычисляем площади подтреугольников
        t1 = Triangle(point, self.p2, self.p3)
        t2 = Triangle(self.p1, point, self.p3)
        t3 = Triangle(self.p1, self.p2, point)

        total_area = self.area()
        return abs(total_area - (t1.area() + t2.area() + t3.area())) < 1e-9


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Треугольник и точки")
        self.root.geometry("900x700")

        self.points = []
        self.triangle = None
        self.speed = tk.DoubleVar(value=1.0)
        self.paused = False
        self.animating = False

        self.setup_ui()
        self.setup_canvas()

    def setup_ui(self):
        # Панель управления
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Координаты треугольника
        ttk.Label(control_frame, text="Треугольник:").grid(
            row=0, column=0, columnspan=3, sticky=tk.W
        )

        ttk.Label(control_frame, text="X1,Y1:").grid(row=1, column=0, sticky=tk.W)
        self.t_p1 = ttk.Entry(control_frame, width=10)
        self.t_p1.grid(row=1, column=1)
        self.t_p1.insert(0, "200,100")

        ttk.Label(control_frame, text="X2,Y2:").grid(row=1, column=2, sticky=tk.W)
        self.t_p2 = ttk.Entry(control_frame, width=10)
        self.t_p2.grid(row=1, column=3)
        self.t_p2.insert(0, "100,400")

        ttk.Label(control_frame, text="X3,Y3:").grid(row=1, column=4, sticky=tk.W)
        self.t_p3 = ttk.Entry(control_frame, width=10)
        self.t_p3.grid(row=1, column=5)
        self.t_p3.insert(0, "500,300")

        # Количество точек
        ttk.Label(control_frame, text="Кол-во точек:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.points_count = ttk.Entry(control_frame, width=10)
        self.points_count.grid(row=2, column=1, pady=5)
        self.points_count.insert(0, "50")

        # Скорость
        ttk.Label(control_frame, text="Скорость:").grid(row=2, column=2, sticky=tk.W)
        self.speed_scale = ttk.Scale(
            control_frame,
            from_=0.1,
            to=5.0,
            variable=self.speed,
            orient=tk.HORIZONTAL,
            length=100,
        )
        self.speed_scale.grid(row=2, column=3, columnspan=2)
        self.speed_label = ttk.Label(control_frame, text="1.0x")
        self.speed_label.grid(row=2, column=5)
        self.speed.trace_add(
            "write",
            lambda *args: self.speed_label.configure(text=f"{self.speed.get():.1f}x"),
        )

        # Кнопки
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=3, column=0, columnspan=6, pady=10)

        ttk.Button(
            btn_frame, text="Создать/Обновить", command=self.create_objects
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="⏯ Пауза/Продолжить", command=self.toggle_pause
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="📸 Скриншот", command=self.take_screenshot).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(btn_frame, text="Очистить", command=self.clear_canvas).pack(
            side=tk.LEFT, padx=5
        )

        # Статистика
        self.stats_label = ttk.Label(control_frame, text="Готов к работе")
        self.stats_label.grid(row=4, column=0, columnspan=6, sticky=tk.W)

    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", width=850, height=500)
        self.canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def parse_point(self, entry_str):
        try:
            x, y = map(float, entry_str.split(","))
            return Point(x, y)
        except:
            return None

    def create_objects(self):
        try:
            # Создаем треугольник
            p1 = self.parse_point(self.t_p1.get())
            p2 = self.parse_point(self.t_p2.get())
            p3 = self.parse_point(self.t_p3.get())

            if not all([p1, p2, p3]):
                messagebox.showerror("Ошибка", "Неверные координаты треугольника")
                return

            self.triangle = Triangle(p1, p2, p3)

            # Создаем точки
            n = int(self.points_count.get())
            self.points = []
            for i in range(n):
                x = random.uniform(50, 800)
                y = random.uniform(50, 450)
                self.points.append(Point(x, y))

            self.draw_scene()
            self.update_stats()

        except ValueError:
            messagebox.showerror("Ошибка", "Неверное количество точек")

    def draw_scene(self):
        self.canvas.delete("all")

        if not self.triangle:
            return

        # Рисуем треугольник
        self.canvas.create_polygon(
            self.triangle.p1.x,
            self.triangle.p1.y,
            self.triangle.p2.x,
            self.triangle.p2.y,
            self.triangle.p3.x,
            self.triangle.p3.y,
            outline="blue",
            fill="lightblue",
            width=2,
        )

        # Рисуем точки
        for point in self.points:
            if self.triangle.is_point_inside(point):
                color = "green"
                size = 6
            else:
                color = "red"
                size = 4

            self.canvas.create_oval(
                point.x - size,
                point.y - size,
                point.x + size,
                point.y + size,
                fill=color,
                outline="black",
            )

        # Подписываем вершины
        for i, p in enumerate([self.triangle.p1, self.triangle.p2, self.triangle.p3]):
            self.canvas.create_text(
                p.x, p.y - 15, text=f"P{i+1}", fill="blue", font=("Arial", 10, "bold")
            )

    def update_stats(self):
        if not self.triangle:
            return

        inside = sum(1 for p in self.points if self.triangle.is_point_inside(p))
        outside = len(self.points) - inside

        self.stats_label.configure(
            text=f"Всего точек: {len(self.points)} | Внутри: {inside} (зеленые) | Снаружи: {outside} (красные)"
        )

    def toggle_pause(self):
        self.paused = not self.paused

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points = []
        self.triangle = None
        self.stats_label.configure(text="Очищено")

    def take_screenshot(self):
        # Получаем координаты холста
        x = self.root.winfo_rootx() + self.canvas.winfo_x() + 10
        y = self.root.winfo_rooty() + self.canvas.winfo_y() + 10
        width = self.canvas.winfo_width() - 20
        height = self.canvas.winfo_height() - 20

        # Делаем скриншот
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

        # Сохраняем в текущую директорию
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)

        self.stats_label.configure(
            text=f"Скриншот сохранен: {os.path.abspath(filename)}"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
