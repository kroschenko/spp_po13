import tkinter as tk
from tkinter import ttk, filedialog
import colorsys


class JuliaSetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Множество Жюлиа")
        self.root.geometry("1000x750")

        # Параметры фрактала
        self.width = 800
        self.height = 600
        self.max_iter = 100
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0

        # Комплексная константа c (определяет форму множества Жюлиа)
        self.c_real = -0.7
        self.c_imag = 0.27015

        # Цветовая схема
        self.color_scheme = "rainbow"

        # Флаг для остановки отрисовки
        self.is_drawing = False

        self.create_ui()
        self.draw_julia()

    def create_ui(self):
        # Панель управления
        control_frame = ttk.Frame(self.root, padding=10)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Параметры c (комплексное число)
        ttk.Label(control_frame, text="c =").grid(row=0, column=0, padx=5)
        self.c_real_var = tk.DoubleVar(value=self.c_real)
        ttk.Entry(control_frame, textvariable=self.c_real_var, width=8).grid(row=0, column=1, padx=2)

        ttk.Label(control_frame, text="+").grid(row=0, column=2)
        self.c_imag_var = tk.DoubleVar(value=self.c_imag)
        ttk.Entry(control_frame, textvariable=self.c_imag_var, width=8).grid(row=0, column=3, padx=2)

        ttk.Label(control_frame, text="i").grid(row=0, column=4)

        # Предустановки
        ttk.Label(control_frame, text="Пресет:").grid(row=0, column=5, padx=10)
        self.preset_var = tk.StringVar(value="custom")
        presets = ttk.Combobox(control_frame, textvariable=self.preset_var,
                               values=["custom", "dendrite", "rabbit", "spiral", "galaxy"],
                               width=10, state="readonly")
        presets.grid(row=0, column=6, padx=5)
        presets.bind("<<ComboboxSelected>>", self.apply_preset)

        # Максимальное число итераций
        ttk.Label(control_frame, text="Итерации:").grid(row=0, column=7, padx=10)
        self.iter_var = tk.IntVar(value=self.max_iter)
        ttk.Spinbox(control_frame, from_=50, to=1000, textvariable=self.iter_var, width=6).grid(row=0, column=8, padx=5)

        # Цветовая схема
        ttk.Label(control_frame, text="Цвета:").grid(row=1, column=0, padx=5, pady=5)
        self.color_var = tk.StringVar(value=self.color_scheme)
        color_combo = ttk.Combobox(control_frame, textvariable=self.color_var,
                                    values=["rainbow", "fire", "ocean", "grayscale", "neon"],
                                    width=10, state="readonly")
        color_combo.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        # Кнопки
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=1, column=3, columnspan=6, padx=10)

        ttk.Button(btn_frame, text="Построить", command=self.draw_julia).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сбросить вид", command=self.reset_view).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Сохранить", command=self.save_image).pack(side=tk.LEFT, padx=5)

        # Canvas
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(canvas_frame, bg="black", width=self.width, height=self.height,
                                highlightthickness=1, highlightbackground="gray")
        self.canvas.pack()

        # Привязка мыши
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        # Информация
        self.info_label = ttk.Label(self.root, text="ЛКМ: перемещение",
                                     font=("Arial", 9))
        self.info_label.pack(pady=5)

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.is_drawing = False
        self.root.destroy()

    def apply_preset(self, event=None):
        preset = self.preset_var.get()
        presets = {
            "dendrite": (-0.123, 0.745),
            "rabbit": (-0.123, 0.745),
            "spiral": (-0.75, 0.1),
            "galaxy": (-0.4, 0.6),
        }
        if preset in presets:
            c_r, c_i = presets[preset]
            self.c_real_var.set(c_r)
            self.c_imag_var.set(c_i)

    def julia(self, z_real, z_imag, c_real, c_imag, max_iter):
        for i in range(max_iter):
            z_real_sq = z_real * z_real
            z_imag_sq = z_imag * z_imag

            if z_real_sq + z_imag_sq > 4.0:
                return i

            z_imag = 2.0 * z_real * z_imag + c_imag
            z_real = z_real_sq - z_imag_sq + c_real

        return max_iter

    def get_color(self, iteration, max_iter):
        if iteration == max_iter:
            return "#000000"

        t = iteration / max_iter

        if self.color_var.get() == "rainbow":
            hue = t * 360
            r, g, b = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
            return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

        elif self.color_var.get() == "fire":
            r = min(255, int(t * 510))
            g = min(255, int((t - 0.5) * 510)) if t > 0.5 else 0
            b = 0
            return f"#{r:02x}{g:02x}{b:02x}"

        elif self.color_var.get() == "ocean":
            r = 0
            g = min(255, int(t * 510))
            b = min(255, int(t * 255 + 128))
            return f"#{r:02x}{g:02x}{b:02x}"

        elif self.color_var.get() == "neon":
            r = int((1 - t) * 255)
            g = int(t * 255)
            b = int((0.5 - abs(t - 0.5)) * 510)
            return f"#{r:02x}{g:02x}{b:02x}"

        else:
            val = int(t * 255)
            return f"#{val:02x}{val:02x}{val:02x}"

    def draw_julia(self):
        # Останавливаем предыдущую отрисовку
        self.is_drawing = False
        self.root.update()
        self.is_drawing = True

        # Очищаем canvas
        self.canvas.delete("all")

        c_real = self.c_real_var.get()
        c_imag = self.c_imag_var.get()
        max_iter = self.iter_var.get()

        # Область комплексной плоскости
        x_min = -2.0 / self.zoom + self.offset_x
        x_max = 2.0 / self.zoom + self.offset_x
        y_min = -1.5 / self.zoom + self.offset_y
        y_max = 1.5 / self.zoom + self.offset_y

        # Рисуем построчно с проверкой состояния
        for py in range(self.height):
            if not self.is_drawing:
                return

            y = y_min + (y_max - y_min) * py / self.height

            for px in range(self.width):
                x = x_min + (x_max - x_min) * px / self.width

                iteration = self.julia(x, y, c_real, c_imag, max_iter)
                color = self.get_color(iteration, max_iter)

                try:
                    self.canvas.create_line(px, py, px + 1, py, fill=color, width=1)
                except tk.TclError:
                    # Canvas закрыт, выходим
                    return

            # Обновляем каждые 20 строк
            if py % 20 == 0:
                try:
                    self.info_label.config(text=f"Рисование... {100 * py // self.height}%")
                    self.root.update()
                except tk.TclError:
                    return

        self.is_drawing = False
        try:
            self.info_label.config(text=f"c = {c_real} + {c_imag}i | Итерации: {max_iter} | Готово")
        except tk.TclError:
            pass

    def reset_view(self):
        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.draw_julia()

    def on_click(self, event):
        self.drag_start = (event.x, event.y)
        self.drag_offset = (self.offset_x, self.offset_y)

    def on_drag(self, event):
        if hasattr(self, 'drag_start') and self.drag_start:
            dx = (event.x - self.drag_start[0]) / self.width * 4.0 / self.zoom
            dy = (event.y - self.drag_start[1]) / self.height * 3.0 / self.zoom
            self.offset_x = self.drag_offset[0] - dx
            self.offset_y = self.drag_offset[1] - dy
            self.draw_julia()

    def on_release(self, event):
        self.drag_start = None

    def save_image(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")],
            title="Сохранить изображение"
        )
        if filename:
            try:
                self.canvas.postscript(file=filename, colormode="color",
                                       width=self.width, height=self.height)
                print(f"Изображение сохранено: {filename}")
            except Exception as e:
                print(f"Ошибка сохранения: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = JuliaSetApp(root)
    root.mainloop()
