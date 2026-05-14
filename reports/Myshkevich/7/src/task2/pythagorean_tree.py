"""Склоненное дерево Пифагора (обдуваемое ветром)."""

import tkinter as tk
from tkinter import ttk
import math
import time
import os
from datetime import datetime


class PythagoreanTree:  # pylint: disable=R0902
    """Класс для генерации дерева Пифагора с эффектом ветра."""

    def __init__(self, canvas, x, y, length, angle, wind=0):  # pylint: disable=R0913,R0917
        """Инициализация дерева."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle
        self.wind = wind
        self.max_depth = 12
        self.left_angle = 45
        self.right_angle = 45
        self.length_ratio = 0.68
        self.color_mode = "gradient"

    def draw(self, params):
        """Рекурсивное рисование дерева."""
        x, y, length, angle, depth = params
        if depth > self.max_depth or length < 2:
            return
        rad = math.radians(angle + self.wind * depth * 0.3)
        x2 = x + length * math.cos(rad)
        y2 = y + length * math.sin(rad)
        color = self._get_color(depth)
        width = max(2, 12 - depth)
        self.canvas.create_line(x, y, x2, y2, fill=color, width=width, capstyle=tk.ROUND)
        left = angle - self.left_angle + self.wind * depth * 0.5
        right = angle + self.right_angle + self.wind * depth * 0.5
        new_len = length * self.length_ratio
        self.draw((x2, y2, new_len, left, depth + 1))
        self.draw((x2, y2, new_len, right, depth + 1))

    def _get_color(self, depth):
        """Получение цвета ветки."""
        if self.color_mode == "gradient":
            if depth < 4:
                return "#5D3A1A"
            if depth < 7:
                return "#8B5A2B"
            if depth < 10:
                return "#228B22"
            return "#32CD32"
        if self.color_mode == "rainbow":
            colors = ["#FF4444", "#FF8844", "#FFFF44", "#44FF44", "#44FFFF", "#4444FF", "#FF44FF"]
            return colors[depth % len(colors)]
        return "#8B4513" if depth < 4 else "#228B22"

    def redraw(self):
        """Перерисовка дерева."""
        self.canvas.delete("all")
        self.draw((self.x, self.y, self.length, self.angle, 0))


class TreeApp:  # pylint: disable=R0902
    """Главное приложение."""

    def __init__(self, app_root):
        """Инициализация приложения."""
        self.root = app_root
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
        self.canvas = None
        self.tree = None
        self.wind_animation = False
        self.length_var = None
        self.depth_var = None
        self.left_var = None
        self.right_var = None
        self.ratio_var = None
        self.wind_var = None
        self.color_mode_var = None
        self.animate_btn = None
        self.info_label = None
        self._setup_window()
        self._create_components()

    def _setup_window(self):
        """Настройка окна.""" 
        self.root.title("Склоненное дерево Пифагора - Обдуваемое ветром")
        self.root.geometry("1100x750")
        self.root.configure(bg="#1e1e2e")

    def _create_components(self):
        """Создание компонентов."""
        self._create_menu()
        self._create_canvas()
        self._create_controls()

        self.tree = PythagoreanTree(self.canvas, self.start_x, self.start_y, self.length, self.angle, self.wind)
        self.tree.max_depth = self.max_depth
        self.tree.left_angle = self.left_angle
        self.tree.right_angle = self.right_angle
        self.tree.length_ratio = self.length_ratio
        self.tree.color_mode = self.color_mode
        self.tree.redraw()

    def _create_menu(self):
        """Создание меню."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Скриншот", command=self.take_screenshot, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")
        self.root.bind("<Control-s>", lambda e: self.take_screenshot())
        self.root.bind("<Control-q>", lambda e: self.root.quit())

    def _create_canvas(self):
        """Создание области для рисования."""
        canvas_frame = tk.Frame(self.root, bg="#1e1e2e")
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="#1a3a1a",
            highlightthickness=2,
            highlightbackground="white",
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_rectangle(
            0, self.canvas_height - 25, self.canvas_width, self.canvas_height, fill="#5D3A1A", outline=""
        )

    def _create_controls(self):
        """Создание панели управления."""
        ctrl = tk.Frame(self.root, width=270, bg="#2e2e3e")
        ctrl.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=10)
        ctrl.pack_propagate(False)
        tk.Label(ctrl, text=" Параметры дерева", font=("Arial", 15, "bold"), bg="#2e2e3e", fg="white").pack(pady=10)
        self._add_length(ctrl)
        self._add_depth(ctrl)
        self._add_left(ctrl)
        self._add_right(ctrl)
        self._add_ratio(ctrl)
        self._add_wind(ctrl)
        self._add_color(ctrl)
        self._add_buttons(ctrl)
        self._add_info(ctrl)
        self._add_tips(ctrl)
        self.root.bind("<space>", lambda e: self.toggle_animation())

    def _add_length(self, parent):
        """Добавление контроля длины."""
        f = tk.Frame(parent, bg="#2e2e3e")
        f.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(f, text=" Длина ствола:", bg="#2e2e3e", fg="white").pack(anchor="w")
        self.length_var = tk.IntVar(value=self.length)
        tk.Scale(
            f,
            from_=60,
            to=160,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            command=self._change_length,
            bg="#2e2e3e",
            fg="white",
            highlightthickness=0,
        ).pack(fill=tk.X)

    def _add_depth(self, parent):
        """Добавление контроля глубины."""
        f = tk.Frame(parent, bg="#2e2e3e")
        f.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(f, text=" Глубина рекурсии:", bg="#2e2e3e", fg="white").pack(anchor="w")
        self.depth_var = tk.IntVar(value=self.max_depth)
        tk.Scale(
            f,
            from_=5,
            to=15,
            orient=tk.HORIZONTAL,
            variable=self.depth_var,
            command=self._change_depth,
            bg="#2e2e3e",
            fg="white",
            highlightthickness=0,
        ).pack(fill=tk.X)

    def _add_left(self, parent):
        """Добавление контроля левого угла."""
        f = tk.Frame(parent, bg="#2e2e3e")
        f.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(f, text=" Угол левой ветки:", bg="#2e2e3e", fg="white").pack(anchor="w")
        self.left_var = tk.IntVar(value=self.left_angle)
        tk.Scale(
            f,
            from_=20,
            to=70,
            orient=tk.HORIZONTAL,
            variable=self.left_var,
            command=self._change_left,
            bg="#2e2e3e",
            fg="white",
            highlightthickness=0,
        ).pack(fill=tk.X)

    def _add_right(self, parent):
        """Добавление контроля правого угла."""
        f = tk.Frame(parent, bg="#2e2e3e")
        f.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(f, text=" Угол правой ветки:", bg="#2e2e3e", fg="white").pack(anchor="w")
        self.right_var = tk.IntVar(value=self.right_angle)
        tk.Scale(
            f,
            from_=20,
            to=70,
            orient=tk.HORIZONTAL,
            variable=self.right_var,
            command=self._change_right,
            bg="#2e2e3e",
            fg="white",
            highlightthickness=0,
        ).pack(fill=tk.X)

    def _add_ratio(self, parent):
        """Добавление контроля коэффициента."""
        f = tk.Frame(parent, bg="#2e2e3e")
        f.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(f, text=" Коэф. уменьшения:", bg="#2e2e3e", fg="white").pack(anchor="w")
        self.ratio_var = tk.DoubleVar(value=self.length_ratio)
        tk.Scale(
            f,
            from_=0.55,
            to=0.8,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            variable=self.ratio_var,
            command=self._change_ratio,
            bg="#2e2e3e",
            fg="white",
            highlightthickness=0,
        ).pack(fill=tk.X)

    def _add_wind(self, parent):
        """Добавление контроля ветра."""
        f = tk.Frame(parent, bg="#2e2e3e")
        f.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(f, text=" Сила ветра:", bg="#2e2e3e", fg="white").pack(anchor="w")
        self.wind_var = tk.IntVar(value=self.wind)
        tk.Scale(
            f,
            from_=-25,
            to=25,
            orient=tk.HORIZONTAL,
            variable=self.wind_var,
            command=self._change_wind,
            bg="#2e2e3e",
            fg="white",
            highlightthickness=0,
        ).pack(fill=tk.X)

    def _add_color(self, parent):
        """Добавление выбора цвета."""
        f = tk.Frame(parent, bg="#2e2e3e")
        f.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(f, text=" Режим цвета:", bg="#2e2e3e", fg="white").pack(anchor="w")
        self.color_mode_var = tk.StringVar(value=self.color_mode)
        cm = ttk.Combobox(f, textvariable=self.color_mode_var, values=["gradient", "rainbow"], state="readonly")
        cm.pack(fill=tk.X)
        cm.bind("<<ComboboxSelected>>", self._change_color)

    def _add_buttons(self, parent):
        """Добавление кнопок."""
        bf = tk.Frame(parent, bg="#2e2e3e")
        bf.pack(pady=10)
        self.animate_btn = tk.Button(
            bf, text="🎐 Анимация ветра", command=self.toggle_animation, bg="#444", fg="white", width=18
        )
        self.animate_btn.pack(pady=3)
        tk.Button(bf, text=" Скриншот", command=self.take_screenshot, bg="#444", fg="white", width=18).pack(pady=3)

    def _add_info(self, parent):
        """Добавление информационной метки."""
        self.info_label = tk.Label(parent, text="", bg="#2e2e3e", fg="white", justify=tk.LEFT, font=("Courier", 9))
        self.info_label.pack(pady=10)

    def _add_tips(self, parent):
        """Добавление подсказок."""
        tip = " Подсказки:\n• Ctrl+S - Скриншот\n• Ctrl+Q - Выход\n• Пробел - Анимация ветра"
        tk.Label(parent, text=tip, bg="#2e2e3e", fg="#aaa", font=("Arial", 9), justify=tk.LEFT).pack(
            side=tk.BOTTOM, pady=20
        )

    def _change_length(self, v):
        """Обработчик изменения длины."""
        self.length = int(v)
        if self.tree:
            self.tree.length = self.length
            self.tree.redraw()
        self._update_info()

    def _change_depth(self, v):
        """Обработчик изменения глубины."""
        self.max_depth = int(v)
        if self.tree:
            self.tree.max_depth = self.max_depth
            self.tree.redraw()
        self._update_info()

    def _change_left(self, v):
        """Обработчик изменения левого угла."""
        self.left_angle = int(v)
        if self.tree:
            self.tree.left_angle = self.left_angle
            self.tree.redraw()
        self._update_info()

    def _change_right(self, v):
        """Обработчик изменения правого угла."""
        self.right_angle = int(v)
        if self.tree:
            self.tree.right_angle = self.right_angle
            self.tree.redraw()
        self._update_info()

    def _change_ratio(self, v):
        """Обработчик изменения коэффициента."""
        self.length_ratio = float(v)
        if self.tree:
            self.tree.length_ratio = self.length_ratio
            self.tree.redraw()
        self._update_info()

    def _change_wind(self, v):
        """Обработчик изменения ветра."""
        self.wind = int(v)
        if self.tree:
            self.tree.wind = self.wind
            self.tree.redraw()
        self._update_info()

    def _change_color(self, event=None):  # pylint: disable=W0613
        """Обработчик изменения цвета."""
        self.color_mode = self.color_mode_var.get()
        if self.tree:
            self.tree.color_mode = self.color_mode
            self.tree.redraw()

    def toggle_animation(self):
        """Включение/выключение анимации ветра."""
        self.wind_animation = not self.wind_animation
        txt = "⏸ Остановить ветер" if self.wind_animation else "🎐 Анимация ветра"
        if self.animate_btn:
            self.animate_btn.config(text=txt)
        if self.wind_animation:
            self._animate_wind()

    def _animate_wind(self):
        """Анимация ветра."""
        if not self.wind_animation:
            return
        wv = int(math.sin(time.time() * 1.5) * 20)
        if self.wind_var:
            self.wind_var.set(wv)
        self._change_wind(wv)
        self.root.after(80, self._animate_wind)

    def take_screenshot(self):
        """Создание скриншота."""
        os.makedirs("screenshots", exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fn = f"screenshots/tree_{ts}.eps"
        if self.canvas:
            self.canvas.postscript(file=fn, colormode="color")
        print(f"Скриншот сохранен: {fn}")

    def _update_info(self):
        """Обновление информации."""
        txt = (
            f" Длина: {self.length}\n Глубина: {self.max_depth}\n"
            f"⬅ Левый угол: {self.left_angle}°\n Правый угол: {self.right_angle}°\n"
            f" Коэф. уменьшения: {self.length_ratio:.2f}\n Ветер: {self.wind}"
        )
        if self.info_label:
            self.info_label.config(text=txt)


if __name__ == "__main__":
    ROOT = tk.Tk()
    TreeApp(ROOT)
    ROOT.mainloop()
