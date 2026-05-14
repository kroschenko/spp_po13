"""Склоненное дерево Пифагора (обдуваемое ветром)."""
import tkinter as tk
from tkinter import ttk
import math
import time
import os
from datetime import datetime


class PythagoreanTree:  # pylint: disable=R0902
    """Класс для генерации дерева Пифагора с эффектом ветра."""

    def __init__(self, canvas, x: int, y: int, length: float,  # pylint: disable=R0913,R0917
                 angle: float, wind: float = 0):
        """Инициализация дерева."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.wind = wind
        self.depth = 0
        self.max_depth = 12
        self.left_angle = 45
        self.right_angle = 45
        self.length_ratio = 0.68
        self.color_mode = "gradient"

    def draw(self, x: float, y: float, length: float,  # pylint: disable=R0913,R0917
             angle: float, depth: int):
        """Рекурсивное рисование дерева."""
        if depth > self.max_depth or length < 2:
            return

        rad = math.radians(angle + self.wind * depth * 0.3)
        x2 = x + length * math.cos(rad)
        y2 = y + length * math.sin(rad)

        color = self._get_color(depth)

        line_width = max(2, 12 - depth)
        self.canvas.create_line(x, y, x2, y2, fill=color,
                                width=line_width, capstyle=tk.ROUND)

        left_angle = angle - self.left_angle + self.wind * depth * 0.5
        right_angle = angle + self.right_angle + self.wind * depth * 0.5

        new_length = length * self.length_ratio
        self.draw(x2, y2, new_length, left_angle, depth + 1)
        self.draw(x2, y2, new_length, right_angle, depth + 1)

    def _get_color(self, depth: int) -> str:
        """Получение цвета в зависимости от глубины и режима."""
        if self.color_mode == "gradient":
            if depth < 4:
                return "#5D3A1A"
            if depth < 7:
                return "#8B5A2B"
            if depth < 10:
                return "#228B22"
            return "#32CD32"
        if self.color_mode == "rainbow":
            colors = ["#FF4444", "#FF8844", "#FFFF44", "#44FF44",
                      "#44FFFF", "#4444FF", "#FF44FF"]
            return colors[depth % len(colors)]
        return "#8B4513" if depth < 4 else "#228B22"

    def redraw(self):
        """Перерисовка дерева."""
        self.canvas.delete("all")
        self.draw(self.x, self.y, self.length, self.angle, 0)


class TreeApp:  # pylint: disable=R0902
    """Главное приложение."""

    def __init__(self, app_root):  # pylint: disable=R0914
        """Инициализация приложения."""
        self.root = app_root
        self.root.title("Склоненное дерево Пифагора - Обдуваемое ветром")
        self.root.geometry("1100x750")
        self.root.configure(bg='#1e1e2e')

        self.canvas_width = 900
        self.canvas_height = 700
        self.start_x = self.canvas_width // 2
        self.start_y = self.canvas_height - 50
        self.length = 100
        self.angle = -90
        self.wind = 0
        self.max_depth = 11
        self.left_angle = 45
        self.right_angle = 45
        self.length_ratio = 0.68
        self.color_mode = "gradient"

        self.length_var = None
        self.depth_var = None
        self.left_var = None
        self.right_var = None
        self.ratio_var = None
        self.wind_var = None
        self.color_mode_var = None
        self.animate_btn = None
        self.info_label = None

        self._create_menu()
        self._create_canvas()
        self._create_controls()

        self.tree = PythagoreanTree(
            self.canvas, self.start_x, self.start_y,
            self.length, self.angle, self.wind
        )
        self.tree.max_depth = self.max_depth
        self.tree.left_angle = self.left_angle
        self.tree.right_angle = self.right_angle
        self.tree.length_ratio = self.length_ratio
        self.tree.color_mode = self.color_mode
        self.tree.redraw()

        self.wind_animation = False

    def _create_menu(self):
        """Создание меню."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Скриншот", command=self.take_screenshot,
                              accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit,
                              accelerator="Ctrl+Q")

        self.root.bind('<Control-s>', lambda e: self.take_screenshot())
        self.root.bind('<Control-q>', lambda e: self.root.quit())

    def _create_canvas(self):
        """Создание области для рисования."""
        canvas_frame = tk.Frame(self.root, bg='#1e1e2e')
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH,
                          expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            canvas_frame, width=self.canvas_width, height=self.canvas_height,
            bg='#1a3a1a', highlightthickness=2, highlightbackground='white'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.create_rectangle(0, self.canvas_height - 25,
                                      self.canvas_width, self.canvas_height,
                                      fill="#5D3A1A", outline="")

    def _create_controls(self):
        """Создание панели управления."""
        ctrl = tk.Frame(self.root, width=270, bg='#2e2e3e')
        ctrl.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=10)
        ctrl.pack_propagate(False)

        tk.Label(ctrl, text="🌳 Параметры дерева",
                 font=('Arial', 15, 'bold'), bg='#2e2e3e',
                 fg='white').pack(pady=10)

        self._add_length_control(ctrl)
        self._add_depth_control(ctrl)
        self._add_left_angle_control(ctrl)
        self._add_right_angle_control(ctrl)
        self._add_ratio_control(ctrl)
        self._add_wind_control(ctrl)
        self._add_color_control(ctrl)
        self._add_buttons(ctrl)
        self._add_info_label(ctrl)
        self._add_tips(ctrl)

        self.root.bind('<space>', lambda e: self.toggle_animation())

    def _add_length_control(self, parent):
        frame = tk.Frame(parent, bg='#2e2e3e')
        frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(frame, text="📏 Длина ствола:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.length_var = tk.IntVar(value=self.length)
        tk.Scale(frame, from_=60, to=160, orient=tk.HORIZONTAL, variable=self.length_var,
                 command=self.change_length, bg='#2e2e3e', fg='white', highlightthickness=0).pack(fill=tk.X)

    def _add_depth_control(self, parent):
        frame = tk.Frame(parent, bg='#2e2e3e')
        frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(frame, text="🔢 Глубина рекурсии:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.depth_var = tk.IntVar(value=self.max_depth)
        tk.Scale(frame, from_=5, to=15, orient=tk.HORIZONTAL, variable=self.depth_var,
                 command=self.change_depth, bg='#2e2e3e', fg='white', highlightthickness=0).pack(fill=tk.X)

    def _add_left_angle_control(self, parent):
        frame = tk.Frame(parent, bg='#2e2e3e')
        frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(frame, text="⬅️ Угол левой ветки:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.left_var = tk.IntVar(value=self.left_angle)
        tk.Scale(frame, from_=20, to=70, orient=tk.HORIZONTAL, variable=self.left_var,
                 command=self.change_left_angle, bg='#2e2e3e', fg='white', highlightthickness=0).pack(fill=tk.X)

    def _add_right_angle_control(self, parent):
        frame = tk.Frame(parent, bg='#2e2e3e')
        frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(frame, text="➡️ Угол правой ветки:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.right_var = tk.IntVar(value=self.right_angle)
        tk.Scale(frame, from_=20, to=70, orient=tk.HORIZONTAL, variable=self.right_var,
                 command=self.change_right_angle, bg='#2e2e3e', fg='white', highlightthickness=0).pack(fill=tk.X)

    def _add_ratio_control(self, parent):
        frame = tk.Frame(parent, bg='#2e2e3e')
        frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(frame, text="📉 Коэф. уменьшения:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.ratio_var = tk.DoubleVar(value=self.length_ratio)
        tk.Scale(frame, from_=0.55, to=0.8, resolution=0.01, orient=tk.HORIZONTAL,
                 variable=self.ratio_var, command=self.change_ratio, bg='#2e2e3e',
                 fg='white', highlightthickness=0).pack(fill=tk.X)

    def _add_wind_control(self, parent):
        frame = tk.Frame(parent, bg='#2e2e3e')
        frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(frame, text="🌬️ Сила ветра:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.wind_var = tk.IntVar(value=self.wind)
        tk.Scale(frame, from_=-25, to=25, orient=tk.HORIZONTAL, variable=self.wind_var,
                 command=self.change_wind, bg='#2e2e3e', fg='white', highlightthickness=0).pack(fill=tk.X)

    def _add_color_control(self, parent):
        frame = tk.Frame(parent, bg='#2e2e3e')
        frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(frame, text="🎨 Режим цвета:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.color_mode_var = tk.StringVar(value=self.color_mode)
        color_menu = ttk.Combobox(frame, textvariable=self.color_mode_var,
                                  values=["gradient", "rainbow"], state="readonly")
        color_menu.pack(fill=tk.X)
        color_menu.bind('<<ComboboxSelected>>', self.change_color_mode)

    def _add_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg='#2e2e3e')
        btn_frame.pack(pady=10)
        self.animate_btn = tk.Button(btn_frame, text="🎐 Анимация ветра", command=self.toggle_animation,
                                     bg='#444', fg='white', width=18)
        self.animate_btn.pack(pady=3)
        tk.Button(btn_frame, text="🔄 Сброс параметров", command=self.reset_params,
                  bg='#444', fg='white', width=18).pack(pady=3)
        tk.Button(btn_frame, text="📸 Скриншот", command=self.take_screenshot,
                  bg='#444', fg='white', width=18).pack(pady=3)

    def _add_info_label(self, parent):
        self.info_label = tk.Label(parent, text="", bg='#2e2e3e', fg='white',
                                   justify=tk.LEFT, font=('Courier', 9))
        self.info_label.pack(pady=10)

    def _add_tips(self, parent):
        tip_text = "💡 Подсказки:\n• Ctrl+S - Скриншот\n• Ctrl+Q - Выход"
        tk.Label(parent, text=tip_text, bg='#2e2e3e', fg='#aaa',
                 font=('Arial', 9), justify=tk.LEFT).pack(side=tk.BOTTOM, pady=20)

    def change_length(self, value):
        self.length = int(value)
        self.tree.length = self.length
        self.tree.redraw()
        self.update_info()

    def change_depth(self, value):
        self.max_depth = int(value)
        self.tree.max_depth = self.max_depth
        self.tree.redraw()
        self.update_info()

    def change_left_angle(self, value):
        self.left_angle = int(value)
        self.tree.left_angle = self.left_angle
        self.tree.redraw()
        self.update_info()

    def change_right_angle(self, value):
        self.right_angle = int(value)
        self.tree.right_angle = self.right_angle
        self.tree.redraw()
        self.update_info()

    def change_ratio(self, value):
        self.length_ratio = float(value)
        self.tree.length_ratio = self.length_ratio
        self.tree.redraw()
        self.update_info()

    def change_wind(self, value):
        self.wind = int(value)
        self.tree.wind = self.wind
        self.tree.redraw()
        self.update_info()

    def change_color_mode(self):
        self.color_mode = self.color_mode_var.get()
        self.tree.color_mode = self.color_mode
        self.tree.redraw()

    def toggle_animation(self):
        self.wind_animation = not self.wind_animation
        text = "⏸ Остановить ветер" if self.wind_animation else "🎐 Анимация ветра"
        self.animate_btn.config(text=text)
        if self.wind_animation:
            self.animate_wind()

    def animate_wind(self):
        if not self.wind_animation:
            return
        wind_value = int(math.sin(time.time() * 1.5) * 20)
        self.wind_var.set(wind_value)
        self.change_wind(wind_value)
        self.root.after(80, self.animate_wind)

    def reset_params(self):
        self.length = 100
        self.max_depth = 11
        self.left_angle = 45
        self.right_angle = 45
        self.length_ratio = 0.68
        self.wind = 0
        self.color_mode = "gradient"
        self.length_var.set(100)
        self.depth_var.set(11)
        self.left_var.set(45)
        self.right_var.set(45)
        self.ratio_var.set(0.68)
        self.wind_var.set(0)
        self.color_mode_var.set("gradient")
        self.tree.length = 100
        self.tree.max_depth = 11
        self.tree.left_angle = 45
        self.tree.right_angle = 45
        self.tree.length_ratio = 0.68
        self.tree.wind = 0
        self.tree.color_mode = "gradient"
        self.tree.redraw()
        self.update_info()

    def take_screenshot(self):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/tree_{timestamp}.eps"
        self.canvas.postscript(file=filename, colormode='color')
        print(f"Скриншот сохранен: {filename}")

    def update_info(self):
        text = (f"📏 Длина: {self.length}\n🔢 Глубина: {self.max_depth}\n"
                f"⬅️ Левый угол: {self.left_angle}°\n➡️ Правый угол: {self.right_angle}°\n"
                f"📉 Коэф. уменьшения: {self.length_ratio:.2f}\n🌬️ Ветер: {self.wind}")
        self.info_label.config(text=text)


if __name__ == "__main__":
    ROOT = tk.Tk()
    TreeApp(ROOT)
    ROOT.mainloop()
