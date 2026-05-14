"""Движущаяся окружность с отражением от границ (tkinter версия)."""
import tkinter as tk
from datetime import datetime
import os


class MovingCircle:  # pylint: disable=R0902
    """Класс окружности с движением и отражением от границ."""

    def __init__(self, canvas, x: int, y: int, radius: int,  # pylint: disable=R0913,R0917
                 speed_x: float, speed_y: float, color: str):
        """Инициализация окружности."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.is_paused = False
        self._screenshot_count = 0
        self.oval_id = None
        self._create_oval()

    def _create_oval(self):
        """Создание окружности на canvas."""
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        self.oval_id = self.canvas.create_oval(
            x1, y1, x2, y2, fill=self.color, outline='white', width=2
        )

    def update(self, delta_time: float, width: int, height: int):
        """Обновление позиции окружности."""
        if self.is_paused:
            return

        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time

        # Левая и правая граница
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x = abs(self.speed_x)
        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.speed_x = -abs(self.speed_x)

        # Верхняя и нижняя граница
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.speed_y = abs(self.speed_y)
        elif self.y + self.radius >= height:
            self.y = height - self.radius
            self.speed_y = -abs(self.speed_y)

        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        self.canvas.coords(self.oval_id, x1, y1, x2, y2)

    def set_speed(self, speed_x: float, speed_y: float):
        """Установка скорости."""
        self.speed_x = speed_x
        self.speed_y = speed_y

    def set_radius(self, radius: int):
        """Установка радиуса."""
        self.radius = radius
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        self.canvas.coords(self.oval_id, x1, y1, x2, y2)

    def set_color(self, color: str):
        """Установка цвета."""
        self.color = color
        self.canvas.itemconfig(self.oval_id, fill=color)

    def toggle_pause(self):
        """Приостановка/возобновление движения."""
        self.is_paused = not self.is_paused
        return self.is_paused

    def draw(self):
        """Отрисовка окружности."""
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        self.canvas.coords(self.oval_id, x1, y1, x2, y2)


class CircleAnimationApp:  # pylint: disable=R0902
    """Главное приложение."""

    def __init__(self, app_root):  # pylint: disable=R0914
        """Инициализация приложения."""
        self.root = app_root
        self.root.title("Движущаяся окружность - Лабораторная работа №7")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1e1e2e')

        # Параметры
        self.width = 700
        self.height = 600
        self.radius = 30
        self.speed_x = 5
        self.speed_y = 3
        self.color = "red"

        self._create_menu()
        self._create_canvas()
        self._create_controls()

        self.circle = MovingCircle(
            self.canvas, self.width // 2, self.height // 2,
            self.radius, self.speed_x, self.speed_y, self.color
        )

        self.is_running = True
        self.last_time = None
        self.animate()

    def _create_menu(self):
        """Создание меню."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Скриншот", command=self.take_screenshot, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")

        self.root.bind('<Control-s>', lambda e: self.take_screenshot())
        self.root.bind('<Control-q>', lambda e: self.root.quit())

    def _create_canvas(self):
        """Создание области для рисования."""
        canvas_frame = tk.Frame(self.root, bg='#1e1e2e')
        canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            canvas_frame, width=self.width, height=self.height,
            bg='#1e1e2e', highlightthickness=2, highlightbackground='white'
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_rectangle(0, 0, self.width, self.height, outline='white', width=2)

    def _create_controls(self):  # pylint: disable=R0914
        """Создание панели управления."""
        control_frame = tk.Frame(self.root, width=250, bg='#2e2e3e')
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=10)
        control_frame.pack_propagate(False)

        tk.Label(control_frame, text="Управление", font=('Arial', 16, 'bold'),
                 bg='#2e2e3e', fg='white').pack(pady=10)

        # Кнопки
        btn_frame = tk.Frame(control_frame, bg='#2e2e3e')
        btn_frame.pack(pady=10)

        self.pause_btn = tk.Button(btn_frame, text="⏸ Пауза", command=self.toggle_pause,
                                   width=10, bg='#444', fg='white')
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        reset_btn = tk.Button(btn_frame, text="🔄 Сброс", command=self.reset,
                              width=10, bg='#444', fg='white')
        reset_btn.pack(side=tk.LEFT, padx=5)

        screenshot_btn = tk.Button(btn_frame, text="📸 Скриншот", command=self.take_screenshot,
                                   width=10, bg='#444', fg='white')
        screenshot_btn.pack(side=tk.LEFT, padx=5)

        tk.Frame(control_frame, height=2, bg='#555').pack(fill=tk.X, pady=10)

        # Радиус
        radius_frame = tk.Frame(control_frame, bg='#2e2e3e')
        radius_frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(radius_frame, text="Радиус:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.radius_var = tk.IntVar(value=self.radius)
        radius_scale = tk.Scale(radius_frame, from_=10, to=100, orient=tk.HORIZONTAL,
                                variable=self.radius_var, command=self.change_radius,
                                bg='#2e2e3e', fg='white', highlightthickness=0)
        radius_scale.pack(fill=tk.X)

        # Скорость X
        speed_x_frame = tk.Frame(control_frame, bg='#2e2e3e')
        speed_x_frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(speed_x_frame, text="Скорость X:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.speed_x_var = tk.IntVar(value=self.speed_x)
        speed_x_scale = tk.Scale(speed_x_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                                 variable=self.speed_x_var, command=self.change_speed_x,
                                 bg='#2e2e3e', fg='white', highlightthickness=0)
        speed_x_scale.pack(fill=tk.X)

        # Скорость Y
        speed_y_frame = tk.Frame(control_frame, bg='#2e2e3e')
        speed_y_frame.pack(fill=tk.X, pady=5, padx=10)
        tk.Label(speed_y_frame, text="Скорость Y:", bg='#2e2e3e', fg='white').pack(anchor='w')
        self.speed_y_var = tk.IntVar(value=self.speed_y)
        speed_y_scale = tk.Scale(speed_y_frame, from_=1, to=50, orient=tk.HORIZONTAL,
                                 variable=self.speed_y_var, command=self.change_speed_y,
                                 bg='#2e2e3e', fg='white', highlightthickness=0)
        speed_y_scale.pack(fill=tk.X)

        tk.Frame(control_frame, height=2, bg='#555').pack(fill=tk.X, pady=10)

        # Цвета
        tk.Label(control_frame, text="Цвет:", bg='#2e2e3e', fg='white').pack(anchor='w', padx=10)
        color_frame = tk.Frame(control_frame, bg='#2e2e3e')
        color_frame.pack(pady=5, padx=10)

        colors = [("🔴 Красный", "red"), ("🟢 Зеленый", "green"), ("🔵 Синий", "blue"),
                  ("🟡 Желтый", "yellow"), ("🟣 Фиолетовый", "purple"),
                  ("🟠 Оранжевый", "orange")]

        for text, color in colors:
            btn = tk.Button(color_frame, text=text, command=lambda c=color: self.change_color(c),
                            bg='#444', fg='white', width=12)
            btn.pack(pady=2)

        tk.Frame(control_frame, height=2, bg='#555').pack(fill=tk.X, pady=10)

        # Информация
        self.info_label = tk.Label(control_frame, text="", bg='#2e2e3e', fg='white',
                                   justify=tk.LEFT, font=('Courier', 10))
        self.info_label.pack(pady=10)

        # Подсказки
        tip_text = ("Подсказки:\n• Пауза/Старт - Пробел\n"
                    "• Ctrl+S - Скриншот\n• Ctrl+Q - Выход")
        tk.Label(control_frame, text=tip_text, bg='#2e2e3e', fg='#aaa',
                 font=('Arial', 9), justify=tk.LEFT).pack(side=tk.BOTTOM, pady=20)

        self.root.bind('<space>', lambda e: self.toggle_pause())

    def change_radius(self, value):
        """Изменение радиуса."""
        self.radius = int(value)
        self.circle.set_radius(self.radius)

    def change_speed_x(self, value):
        """Изменение скорости X."""
        self.speed_x = int(value)
        self.circle.set_speed(self.speed_x, self.speed_y)

    def change_speed_y(self, value):
        """Изменение скорости Y."""
        self.speed_y = int(value)
        self.circle.set_speed(self.speed_x, self.speed_y)

    def change_color(self, color):
        """Изменение цвета."""
        self.color = color
        self.circle.set_color(color)

    def toggle_pause(self):
        """Переключение паузы."""
        paused = self.circle.toggle_pause()
        self.pause_btn.config(text="▶ Старт" if paused else "⏸ Пауза")

    def reset(self):
        """Сброс параметров."""
        self.radius = 30
        self.speed_x = 5
        self.speed_y = 3
        self.color = "red"

        self.radius_var.set(30)
        self.speed_x_var.set(5)
        self.speed_y_var.set(3)

        self.circle.set_radius(30)
        self.circle.set_speed(5, 3)
        self.circle.set_color("red")

        if self.circle.is_paused:
            self.circle.is_paused = False
            self.pause_btn.config(text="⏸ Пауза")

        self.circle.x = self.width // 2
        self.circle.y = self.height // 2
        self.circle.draw()

    def take_screenshot(self):
        """Создание скриншота."""
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/screenshot_{timestamp}.eps"
        self.canvas.postscript(file=filename, colormode='color')
        print(f"Скриншот сохранен: {filename}")

    def update_info(self):
        """Обновление информационной панели."""
        status = "⏸ ПАУЗА" if self.circle.is_paused else "▶ ДВИЖЕНИЕ"
        text = (f"Статус: {status}\nПозиция: ({int(self.circle.x)}, {int(self.circle.y)})\n"
                f"Радиус: {self.circle.radius}\nСкорость: ({self.circle.speed_x}, {self.circle.speed_y})")
        self.info_label.config(text=text)

    def animate(self):
        """Основной цикл анимации."""
        if not self.is_running:
            return

        current_time = self.root.tk.call('clock', 'milliseconds')
        if self.last_time is None:
            self.last_time = current_time
        delta_time = (current_time - self.last_time) / 1000.0
        self.last_time = current_time

        delta_time = min(delta_time, 0.05)

        self.circle.update(delta_time, self.width, self.height)
        self.update_info()
        self.root.after(20, self.animate)


if __name__ == "__main__":
    ROOT = tk.Tk()
    CircleAnimationApp(ROOT)
    ROOT.mainloop()
