import os
from datetime import datetime
import colorsys
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from PIL import Image, ImageTk, ImageGrab


class MandelbrotSet:
    def __init__(self, width=800, height=600, max_iter=100):
        self.width = width
        self.height = height
        self.max_iter = max_iter
        self.zoom = 1.0
        self.offset_x = -0.5
        self.offset_y = 0.0

    def generate(self):
        """Генерирует массив итераций для множества Мандельброта"""
        # Создаем сетку координат
        x = np.linspace(
            -2.5 / self.zoom + self.offset_x,
            1.5 / self.zoom + self.offset_x,
            self.width,
        )
        y = np.linspace(
            -2.0 / self.zoom + self.offset_y,
            2.0 / self.zoom + self.offset_y,
            self.height,
        )

        # Создаем матрицы
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C, dtype=np.complex128)

        # Матрица для хранения количества итераций
        iterations = np.zeros(C.shape, dtype=np.int32)

        # Вычисляем множество Мандельброта
        mask = np.ones(C.shape, dtype=bool)

        for _ in range(self.max_iter):
            Z[mask] = Z[mask] ** 2 + C[mask]
            mask = np.abs(Z) < 2
            iterations += mask

        return iterations

    def zoom_in(self, x, y, factor=2.0):
        """Приближение к указанной точке"""
        # Конвертируем координаты холста в комплексную плоскость
        complex_x = (x - self.width / 2) / (self.width / 4) / self.zoom + self.offset_x
        complex_y = (y - self.height / 2) / (
            self.height / 4
        ) / self.zoom + self.offset_y

        self.zoom *= factor
        self.offset_x = complex_x
        self.offset_y = complex_y

    def reset_view(self):
        """Сброс параметров отображения"""
        self.zoom = 1.0
        self.offset_x = -0.5
        self.offset_y = 0.0


class MandelbrotApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Множество Мандельброта")
        self.master.geometry("1000x800")

        # Параметры фрактала
        self.width = 800
        self.height = 600
        self.max_iter = tk.IntVar(value=100)
        self.color_scheme = tk.StringVar(value="rainbow")
        self.zoom_factor = tk.DoubleVar(value=2.0)
        self.paused = False
        self.drag_start = None
        self.photo = None

        # Создаем объект фрактала
        self.mandelbrot = MandelbrotSet(self.width, self.height, self.max_iter.get())

        # Флаг для отмены вычислений
        self.computing = False

        self._setup_ui()

    def _setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = ttk.Frame(self.master, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_control_panel(main_frame)
        self._create_canvas(main_frame)

        # Генерируем начальный фрактал
        self.master.after(100, self.redraw)

    def _create_control_panel(self, parent):
        """Создание панели управления"""
        control_frame = ttk.LabelFrame(parent, text="Управление", padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))

        self._create_iteration_controls(control_frame)
        self._create_color_controls(control_frame)
        self._create_zoom_controls(control_frame)
        self._create_action_buttons(control_frame)
        self._create_info_labels(control_frame)

    def _create_iteration_controls(self, frame):
        """Создание элементов управления итерациями"""
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=5)

        ttk.Label(row, text="Итерации:").pack(side=tk.LEFT, padx=5)
        self.iter_entry = ttk.Entry(row, textvariable=self.max_iter, width=10)
        self.iter_entry.pack(side=tk.LEFT, padx=5)

    def _create_color_controls(self, frame):
        """Создание элементов управления цветом"""
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=5)

        ttk.Label(row, text="Цветовая схема:").pack(side=tk.LEFT, padx=5)
        color_combo = ttk.Combobox(
            row,
            textvariable=self.color_scheme,
            values=["rainbow", "fire", "ocean", "grayscale", "neon"],
            width=15,
            state="readonly",
        )
        color_combo.pack(side=tk.LEFT, padx=5)
        color_combo.set("rainbow")

        ttk.Label(row, text="Масштаб:").pack(side=tk.LEFT, padx=5)
        self.zoom_label = ttk.Label(row, text="1.0x")
        self.zoom_label.pack(side=tk.LEFT, padx=5)

    def _create_zoom_controls(self, frame):
        """Создание элементов управления зумом"""
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=5)

        ttk.Label(row, text="Фактор зума:").pack(side=tk.LEFT, padx=5)
        zoom_scale = ttk.Scale(
            row,
            from_=1.5,
            to=10.0,
            variable=self.zoom_factor,
            orient=tk.HORIZONTAL,
            length=150,
        )
        zoom_scale.pack(side=tk.LEFT, padx=5)
        self.zoom_factor_label = ttk.Label(row, text="2.0x")
        self.zoom_factor_label.pack(side=tk.LEFT, padx=5)
        self.zoom_factor.trace_add(
            "write",
            lambda *args: self.zoom_factor_label.configure(
                text=f"{self.zoom_factor.get():.1f}x"
            ),
        )

    def _create_action_buttons(self, frame):
        """Создание кнопок действий"""
        row = ttk.Frame(frame)
        row.pack(fill=tk.X, pady=5)

        ttk.Button(row, text="🔄 Перерисовать", command=self.redraw).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(row, text="⏯ Пауза", command=self.toggle_pause).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(row, text="🔍 Сбросить вид", command=self.reset_view).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(row, text="📸 Скриншот", command=self.take_screenshot).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(row, text="💾 Сохранить изображение", command=self.save_image).pack(
            side=tk.LEFT, padx=5
        )

    def _create_info_labels(self, frame):
        """Создание информационных меток"""
        self.info_label = ttk.Label(
            frame, text="Готов к работе. Кликните для приближения"
        )
        self.info_label.pack(fill=tk.X, pady=5)

        self.stats_label = ttk.Label(frame, text="")
        self.stats_label.pack(fill=tk.X)

    def _create_canvas(self, parent):
        """Создание холста для отображения"""
        self.canvas = tk.Canvas(
            parent, width=self.width, height=self.height, bg="black", cursor="crosshair"
        )
        self.canvas.pack(expand=True)

        # Привязка событий мыши
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)

    def _get_color(self, iterations, max_iter):
        """Получение цвета в зависимости от схемы"""
        if iterations == max_iter:
            return (0, 0, 0)  # Черный для точек множества

        ratio = iterations / max_iter

        color_schemes = {
            "rainbow": self._rainbow_color,
            "fire": self._fire_color,
            "ocean": self._ocean_color,
            "neon": self._neon_color,
            "grayscale": self._grayscale_color,
        }

        color_func = color_schemes.get(self.color_scheme.get(), self._grayscale_color)
        return color_func(ratio)

    def _rainbow_color(self, ratio):
        """Радужная цветовая схема"""
        hue = ratio * 0.7
        return tuple(int(255 * c) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0))

    def _fire_color(self, ratio):
        """Огненная цветовая схема"""
        r = min(255, int(ratio * 500))
        g = min(255, int(ratio * 200))
        b = min(255, int(ratio * 50))
        return (r, g, b)

    def _ocean_color(self, ratio):
        """Океанская цветовая схема"""
        r = min(255, int(ratio * 100))
        g = min(255, int(ratio * 200))
        b = min(255, int(ratio * 400))
        return (r, g, b)

    def _neon_color(self, ratio):
        """Неоновая цветовая схема"""
        hue = ratio * 0.8 + 0.6
        saturation = 0.8 + 0.2 * np.sin(ratio * 10)
        return tuple(int(255 * c) for c in colorsys.hsv_to_rgb(hue, saturation, 1.0))

    def _grayscale_color(self, ratio):
        """Черно-белая цветовая схема"""
        v = int(255 * (1 - ratio))
        return (v, v, v)

    def redraw(self):
        """Перерисовка фрактала"""
        if self.computing:
            return

        self.computing = True
        self.info_label.configure(text="Вычисление... Пожалуйста, подождите")
        self.master.update()

        try:
            # Обновляем параметры
            self.mandelbrot.max_iter = self.max_iter.get()

            # Генерируем фрактал
            iterations = self.mandelbrot.generate()

            # Создаем изображение
            image = self._create_fractal_image(iterations)

            # Отображаем на холсте
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(self.width / 2, self.height / 2, image=self.photo)

            # Обновляем статистику
            self._update_statistics(iterations)

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Ошибка в параметрах: {str(e)}")
        except MemoryError:
            messagebox.showerror("Ошибка", "Недостаточно памяти для вычислений")
        finally:
            self.computing = False
            self.info_label.configure(text="Готово. Кликните для приближения")

    def _create_fractal_image(self, iterations):
        """Создание изображения фрактала"""
        image = Image.new("RGB", (self.width, self.height))
        pixels = image.load()

        for y in range(self.height):
            for x in range(self.width):
                color = self._get_color(iterations[y, x], self.max_iter.get())
                pixels[x, y] = color

        return image

    def _update_statistics(self, iterations):
        """Обновление статистической информации"""
        points_in_set = np.sum(iterations == self.max_iter.get())
        total_points = self.width * self.height
        percentage = (points_in_set / total_points) * 100

        self.stats_label.configure(
            text=f"Точек в множестве: {points_in_set} ({percentage:.1f}%) | "
            f"Масштаб: {self.mandelbrot.zoom:.2f}x | "
            f"Смещение: ({self.mandelbrot.offset_x:.4f}, {self.mandelbrot.offset_y:.4f})"
        )

        self.zoom_label.configure(text=f"{self.mandelbrot.zoom:.2f}x")

    def _on_canvas_click(self, event):
        """Обработка клика для зума"""
        if not self.paused:
            self.mandelbrot.zoom_in(event.x, event.y, self.zoom_factor.get())
            self.redraw()

    def _on_canvas_drag(self, event):
        """Обработка перетаскивания"""
        if self.drag_start is None:
            self.drag_start = (event.x, event.y)

    def _on_canvas_release(self, event):
        """Обработка отпускания кнопки мыши"""
        if self.drag_start:
            dx = event.x - self.drag_start[0]
            dy = event.y - self.drag_start[1]

            if abs(dx) > 5 or abs(dy) > 5:  # Минимальное расстояние для перетаскивания
                # Перемещение вида
                scale = 4.0 / (self.width * self.mandelbrot.zoom)
                self.mandelbrot.offset_x -= dx * scale
                self.mandelbrot.offset_y -= dy * scale
                self.redraw()

            self.drag_start = None

    def toggle_pause(self):
        """Пауза/продолжение"""
        self.paused = not self.paused
        if self.paused:
            self.info_label.configure(text="ПАУЗА - интерактивность отключена")
        else:
            self.info_label.configure(text="Работа возобновлена")

    def reset_view(self):
        """Сброс вида"""
        self.mandelbrot.reset_view()
        self.max_iter.set(100)
        self.redraw()

    def take_screenshot(self):
        """Создание скриншота"""
        try:
            x = self.master.winfo_rootx() + self.canvas.winfo_x() + 10
            y = self.master.winfo_rooty() + self.canvas.winfo_y() + 10
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()

            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mandelbrot_screenshot_{timestamp}.png"
            screenshot.save(filename)

            self.info_label.configure(
                text=f"Скриншот сохранен: {os.path.abspath(filename)}"
            )
        except (IOError, OSError) as e:
            messagebox.showerror("Ошибка", f"Не удалось создать скриншот: {str(e)}")

    def save_image(self):
        """Сохранение изображения в высоком качестве"""
        try:
            # Создаем изображение в высоком разрешении
            hd_width, hd_height = self.width * 2, self.height * 2

            mandelbrot_hd = MandelbrotSet(hd_width, hd_height, self.max_iter.get())
            mandelbrot_hd.zoom = self.mandelbrot.zoom
            mandelbrot_hd.offset_x = self.mandelbrot.offset_x
            mandelbrot_hd.offset_y = self.mandelbrot.offset_y

            self.info_label.configure(text="Сохранение в HD качестве...")
            self.master.update()

            iterations = mandelbrot_hd.generate()

            image = Image.new("RGB", (hd_width, hd_height))
            pixels = image.load()

            for y in range(hd_height):
                for x in range(hd_width):
                    color = self._get_color(iterations[y, x], self.max_iter.get())
                    pixels[x, y] = color

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mandelbrot_hd_{timestamp}.png"
            image.save(filename, quality=95)

            self.info_label.configure(
                text=f"HD изображение сохранено: {os.path.abspath(filename)}"
            )

        except (IOError, OSError, MemoryError) as e:
            messagebox.showerror(
                "Ошибка", f"Не удалось сохранить изображение: {str(e)}"
            )


def main():
    """Главная функция для запуска приложения"""
    root = tk.Tk()
    app = MandelbrotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
