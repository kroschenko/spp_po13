"""Класс движущейся окружности (для tkinter)."""


class MovingCircle:  # pylint: disable=R0902
    """Класс окружности с движением и отражением от границ."""

    def __init__(self, canvas, x: int, y: int, radius: int,  # pylint: disable=R0913,R0917
                 speed_x: float, speed_y: float, color: str):
        """
        Инициализация окружности.

        Args:
            canvas: Объект Canvas tkinter
            x: Начальная координата X
            y: Начальная координата Y
            radius: Радиус окружности
            speed_x: Скорость по X (пикселей в секунду)
            speed_y: Скорость по Y (пикселей в секунду)
            color: Цвет в формате строки (например, "red", "#FF0000")
        """
        self.canvas = canvas
        self.x = x
        self.y = y
        self.radius = radius
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.is_paused = False
        self.oval_id = None
        self._create_oval()

    def _create_oval(self):
        """Создание окружности на canvas."""
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        self.oval_id = self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=self.color,
            outline='white',
            width=2
        )

    def update(self, delta_time: float, width: int, height: int):
        """
        Обновление позиции окружности с учетом отражения.

        Args:
            delta_time: Время с предыдущего кадра (секунды)
            width: Ширина экрана
            height: Высота экрана
        """
        if self.is_paused:
            return

        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time

        self._check_boundaries(width, height)
        self._update_canvas_position()

    def _check_boundaries(self, width: int, height: int):
        """Проверка столкновения с границами."""
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

    def _update_canvas_position(self):
        """Обновление позиции на canvas."""
        x1 = self.x - self.radius
        y1 = self.y - self.radius
        x2 = self.x + self.radius
        y2 = self.y + self.radius
        self.canvas.coords(self.oval_id, x1, y1, x2, y2)

    def draw(self):
        """Отрисовка окружности на экране (обновление позиции)."""
        self._update_canvas_position()

    def set_speed(self, speed_x: float, speed_y: float):
        """Установка скорости."""
        self.speed_x = speed_x
        self.speed_y = speed_y

    def set_position(self, x: int, y: int):
        """Установка позиции."""
        self.x = x
        self.y = y

    def set_radius(self, radius: int):
        """Установка радиуса."""
        self.radius = radius
        self.draw()

    def set_color(self, color: str):
        """Установка цвета."""
        self.color = color
        self.canvas.itemconfig(self.oval_id, fill=color)

    def toggle_pause(self):
        """Приостановка/возобновление движения."""
        self.is_paused = not self.is_paused
        return self.is_paused

    def take_screenshot(self, filename: str = "screenshot") -> str:
        """
        Создание скриншота.

        Args:
            filename: Имя файла для сохранения

        Returns:
            Имя сохраненного файла
        """
        if not hasattr(self, '_screenshot_count'):
            self._screenshot_count = 0  # pylint: disable=W0201
        self._screenshot_count += 1
        filename = f"{filename}_{self._screenshot_count:04d}.ps"
        self.canvas.postscript(file=filename, colormode='color')
        return filename
