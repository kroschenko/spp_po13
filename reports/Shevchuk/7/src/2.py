"""Лабораторная работа 7, задание 2, вариант 7.

Построение фрактала: снежинка Коха.
"""

from dataclasses import dataclass
from datetime import datetime
from math import cos, radians, sin, sqrt
from pathlib import Path
import tkinter as tk


@dataclass
class Point:
    """Точка на плоскости."""

    x: float
    y: float


def rotate_point(point: Point, center: Point, angle_degrees: float) -> Point:
    """Поворачивает точку вокруг центра."""
    angle = radians(angle_degrees)
    dx = point.x - center.x
    dy = point.y - center.y

    return Point(
        center.x + dx * cos(angle) - dy * sin(angle),
        center.y + dx * sin(angle) + dy * cos(angle),
    )


def divide_segment(start: Point, end: Point) -> tuple[Point, Point]:
    """Возвращает точки, делящие отрезок на три части."""
    first = Point(
        start.x + (end.x - start.x) / 3,
        start.y + (end.y - start.y) / 3,
    )
    second = Point(
        start.x + 2 * (end.x - start.x) / 3,
        start.y + 2 * (end.y - start.y) / 3,
    )

    return first, second


def koch_curve(start: Point, end: Point, depth: int) -> list[Point]:
    """Строит точки кривой Коха."""
    if depth == 0:
        return [start, end]

    first, second = divide_segment(start, end)
    peak = rotate_point(second, first, -60)

    points = []
    points.extend(koch_curve(start, first, depth - 1)[:-1])
    points.extend(koch_curve(first, peak, depth - 1)[:-1])
    points.extend(koch_curve(peak, second, depth - 1)[:-1])
    points.extend(koch_curve(second, end, depth - 1))

    return points


def koch_snowflake_points(center: Point, size: float, depth: int) -> list[Point]:
    """Возвращает точки снежинки Коха."""
    height = size * sqrt(3) / 2

    first = Point(center.x - size / 2, center.y + height / 3)
    second = Point(center.x + size / 2, center.y + height / 3)
    third = Point(center.x, center.y - 2 * height / 3)

    result = []

    for start, end in [(first, second), (second, third), (third, first)]:
        curve = koch_curve(start, end, depth)

        if result:
            result.extend(curve[1:])
        else:
            result.extend(curve)

    return result


class KochSnowflakeApp:
    """Оконное приложение для построения снежинки Коха."""

    def __init__(self) -> None:
        """Создает окно приложения."""
        self.root = tk.Tk()
        self.root.title("ЛР7. Задание 2. Снежинка Коха")

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        panel = tk.Frame(self.root)
        panel.pack(pady=5)

        tk.Label(panel, text="Глубина:").grid(row=0, column=0, padx=5)
        self.depth_spinbox = tk.Spinbox(panel, from_=0, to=5, width=5)
        self.depth_spinbox.grid(row=0, column=1, padx=5)
        self.depth_spinbox.delete(0, tk.END)
        self.depth_spinbox.insert(0, "3")

        tk.Label(panel, text="Размер:").grid(row=0, column=2, padx=5)
        self.size_scale = tk.Scale(panel, from_=100, to=450, orient=tk.HORIZONTAL)
        self.size_scale.set(350)
        self.size_scale.grid(row=0, column=3, padx=5)

        tk.Button(panel, text="Построить", command=self.draw_fractal).grid(row=0, column=4, padx=5)
        tk.Button(panel, text="Очистить", command=self.clear_canvas).grid(row=0, column=5, padx=5)
        tk.Button(panel, text="Скриншот", command=self.save_screenshot).grid(row=0, column=6, padx=5)

        self.draw_fractal()

    def clear_canvas(self) -> None:
        """Очищает холст."""
        self.canvas.delete("all")

    def save_screenshot(self) -> None:
        """Сохраняет изображение canvas в текущую папку."""
        file_name = f"task2_screenshot_{datetime.now().strftime('%H_%M_%S')}.ps"
        self.canvas.postscript(file=str(Path.cwd() / file_name), colormode="color")

    def draw_fractal(self) -> None:
        """Рисует снежинку Коха."""
        self.canvas.delete("all")

        depth = int(self.depth_spinbox.get())
        size = self.size_scale.get()
        points = koch_snowflake_points(Point(400, 320), size, depth)

        for index in range(len(points) - 1):
            start = points[index]
            end = points[index + 1]
            self.canvas.create_line(start.x, start.y, end.x, end.y, fill="blue", width=1)

        self.canvas.create_text(
            400,
            30,
            text=f"Снежинка Коха. Глубина: {depth}",
            font=("Arial", 16),
        )

    def run(self) -> None:
        """Запускает приложение."""
        self.root.mainloop()


if __name__ == "__main__":
    KochSnowflakeApp().run()
