import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import math
import time


class RotatingRectangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Вращающийся прямоугольник")
        self.root.geometry("900x700")

        # Параметры прямоугольника
        self.center_x = 400
        self.center_y = 350
        self.width = 150
        self.height = 100
        self.angle = 0
        self.rotation_speed = 2  # градусов за кадр
        self.rotation_center = "top_left"  # вершина вращения

        # Цвета
        self.fill_color = "#3498db"
        self.outline_color = "#2c3e50"

        # Состояние анимации
        self.is_running = False
        self.is_paused = False

        self.create_ui()
        self.draw_rectangle()

    def create_ui(self):
        # Панель управления
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Ширина
        ttk.Label(control_frame, text="Ширина:").grid(row=0, column=0, padx=5)
        self.width_var = tk.IntVar(value=self.width)
        width_spin = ttk.Spinbox(control_frame, from_=50, to=300, textvariable=self.width_var, width=8)
        width_spin.grid(row=0, column=1, padx=5)

        # Высота
        ttk.Label(control_frame, text="Высота:").grid(row=0, column=2, padx=5)
        self.height_var = tk.IntVar(value=self.height)
        height_spin = ttk.Spinbox(control_frame, from_=50, to=300, textvariable=self.height_var, width=8)
        height_spin.grid(row=0, column=3, padx=5)

        # Скорость
        ttk.Label(control_frame, text="Скорость:").grid(row=0, column=4, padx=5)
        self.speed_var = tk.IntVar(value=self.rotation_speed)
        speed_spin = ttk.Spinbox(control_frame, from_=1, to=20, textvariable=self.speed_var, width=8)
        speed_spin.grid(row=0, column=5, padx=5)

        # Точка вращения
        ttk.Label(control_frame, text="Точка вращения:").grid(row=1, column=0, padx=5, pady=5)
        self.rotation_var = tk.StringVar(value=self.rotation_center)
        rotation_combo = ttk.Combobox(control_frame, textvariable=self.rotation_var,
                                       values=["top_left", "top_right", "bottom_left", "bottom_right", "center"],
                                       width=12, state="readonly")
        rotation_combo.grid(row=1, column=1, padx=5, pady=5)

        # Кнопки цвета
        ttk.Button(control_frame, text="Цвет заливки", command=self.choose_fill_color).grid(row=1, column=2, padx=5)
        ttk.Button(control_frame, text="Цвет контура", command=self.choose_outline_color).grid(row=1, column=3, padx=5)

        # Кнопки управления
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=1, column=4, columnspan=3, padx=10)

        self.start_btn = ttk.Button(btn_frame, text="Старт", command=self.start_animation)
        self.start_btn.pack(side=tk.LEFT, padx=2)

        self.pause_btn = ttk.Button(btn_frame, text="Пауза", command=self.toggle_pause, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=2)

        self.stop_btn = ttk.Button(btn_frame, text="Стоп", command=self.stop_animation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)

        ttk.Button(btn_frame, text="Скриншот", command=self.take_screenshot).pack(side=tk.LEFT, padx=2)

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=1, highlightbackground="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Привязка изменений
        self.width_var.trace("w", self.on_param_change)
        self.height_var.trace("w", self.on_param_change)
        self.speed_var.trace("w", self.on_param_change)
        self.rotation_var.trace("w", self.on_param_change)

    def choose_fill_color(self):
        color = colorchooser.askcolor(title="Выберите цвет заливки", initialcolor=self.fill_color)
        if color[1]:
            self.fill_color = color[1]
            self.draw_rectangle()

    def choose_outline_color(self):
        color = colorchooser.askcolor(title="Выберите цвет контура", initialcolor=self.outline_color)
        if color[1]:
            self.outline_color = color[1]
            self.draw_rectangle()

    def on_param_change(self, *args):
        try:
            self.width = int(self.width_var.get())
            self.height = int(self.height_var.get())
            self.rotation_speed = int(self.speed_var.get())
            self.rotation_center = self.rotation_var.get()
            if not self.is_running:
                self.draw_rectangle()
        except ValueError:
            pass

    def get_rectangle_points(self, cx, cy, w, h, angle_deg):
        # Получить координаты вершин прямоугольника с учетом поворота
        angle_rad = math.radians(angle_deg)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # Вершины относительно центра
        half_w = w / 2
        half_h = h / 2

        corners = [
            (-half_w, -half_h),  # top-left
            (half_w, -half_h),   # top-right
            (half_w, half_h),    # bottom-right
            (-half_w, half_h)    # bottom-left
        ]

        rotated_corners = []
        for x, y in corners:
            new_x = x * cos_a - y * sin_a
            new_y = x * sin_a + y * cos_a
            rotated_corners.append((cx + new_x, cy + new_y))

        return rotated_corners

    def get_rotation_point(self, corners):
        # Получить точку вращения по углам
        if self.rotation_center == "top_left":
            return corners[0]
        elif self.rotation_center == "top_right":
            return corners[1]
        elif self.rotation_center == "bottom_right":
            return corners[2]
        elif self.rotation_center == "bottom_left":
            return corners[3]
        else:  # center
            # Вычисляем центр
            x = sum(c[0] for c in corners) / 4
            y = sum(c[1] for c in corners) / 4
            return (x, y)

    def draw_rectangle(self):
        self.canvas.delete("all")

        # Получаем точки прямоугольника
        corners = self.get_rectangle_points(self.center_x, self.center_y, self.width, self.height, self.angle)

        # Рисуем прямоугольник
        points = []
        for x, y in corners:
            points.extend([x, y])

        self.canvas.create_polygon(points, fill=self.fill_color, outline=self.outline_color, width=3)

        # Рисуем точку вращения
        rot_point = self.get_rotation_point(corners)
        self.canvas.create_oval(rot_point[0]-5, rot_point[1]-5, rot_point[0]+5, rot_point[1]+5,
                                fill="red", outline="darkred")

        # Подпись
        self.canvas.create_text(self.center_x, 30, text=f"Угол: {self.angle:.1f}°", font=("Arial", 12))
        self.canvas.create_text(self.center_x, 50, text=f"Точка вращения: {self.rotation_center}", font=("Arial", 10))

    def start_animation(self):
        self.is_running = True
        self.is_paused = False
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL, text="Пауза")
        self.stop_btn.config(state=tk.NORMAL)
        self.animate()

    def toggle_pause(self):
        if self.is_paused:
            self.is_paused = False
            self.pause_btn.config(text="Пауза")
            self.animate()
        else:
            self.is_paused = True
            self.pause_btn.config(text="Продолжить")

    def stop_animation(self):
        self.is_running = False
        self.is_paused = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED, text="Пауза")
        self.stop_btn.config(state=tk.DISABLED)

    def animate(self):
        if self.is_running and not self.is_paused:
            self.angle = (self.angle + self.rotation_speed) % 360
            self.draw_rectangle()
            self.root.after(30, self.animate)  # ~33 FPS

    def take_screenshot(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")],
            title="Сохранить скриншот"
        )
        if filename:
            self.canvas.postscript(file=filename, colormode="color")
            print(f"Скриншот сохранен: {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RotatingRectangleApp(root)
    root.mainloop()
