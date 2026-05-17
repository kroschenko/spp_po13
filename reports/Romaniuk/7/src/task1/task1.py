import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
from datetime import datetime


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def side_of_line(self, line):
        x1, y1 = line.p1.x, line.p1.y
        x2, y2 = line.p2.x, line.p2.y
        value = (x2 - x1) * (self.y - y1) - (y2 - y1) * (self.x - x1)
        if value > 0:
            return 1
        if value < 0:
            return -1
        return 0

    def get_coordinates(self):
        return (self.x, self.y)


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def is_near(self, point, threshold=20):
        x1, y1 = self.p1.x, self.p1.y
        x2, y2 = self.p2.x, self.p2.y
        x0, y0 = point.x, point.y
        dist = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        dist = dist / math.hypot(y2 - y1, x2 - x1)
        return dist <= threshold

    def length(self):
        return math.hypot(self.p2.x - self.p1.x, self.p2.y - self.p1.y)


class PointSideCalculator:
    @staticmethod
    def get_side_color(point, line):
        if not line:
            return "black"
        side = point.side_of_line(line)
        if side == 1:
            return "green"
        if side == -1:
            return "blue"
        return "orange"

    @staticmethod
    def classify_points(points, line):
        side1, side2, on_line = [], [], []
        for point in points:
            coord_str = f"({point.x},{point.y})"
            side = point.side_of_line(line)
            if side == 1:
                side1.append(coord_str)
            elif side == -1:
                side2.append(coord_str)
            else:
                on_line.append(coord_str)
        return side1, side2, on_line


class LineDrawer:
    @staticmethod
    def draw_line_with_labels(canvas, line):
        if not line:
            return
        x1, y1 = line.p1.x, line.p1.y
        x2, y2 = line.p2.x, line.p2.y
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        nx, ny = -dy, dx
        length = math.hypot(nx, ny)
        if length != 0:
            nx, ny = nx / length * 20, ny / length * 20
            canvas.create_text(mx + nx, my + ny, text="Side +1", fill="green")
            canvas.create_text(mx - nx, my - ny, text="Side -1", fill="blue")

    @staticmethod
    def draw_points(canvas, points, line):
        for i, point in enumerate(points):
            color = PointSideCalculator.get_side_color(point, line)
            canvas.create_oval(point.x - 4, point.y - 4, point.x + 4, point.y + 4, fill=color, outline="black")
            canvas.create_text(point.x + 8, point.y - 8, text=str(i + 1), font=("Arial", 8))


class AnimationManager:
    def __init__(self, canvas, points, get_speed):
        self.canvas = canvas
        self.points = points
        self.get_speed = get_speed
        self.running = False
        self.index = 0

    def start(self):
        self.running = True
        self.index = 0
        self._animate()

    def stop(self):
        self.running = False

    def _animate(self):
        if not self.running:
            return
        if self.index < len(self.points):
            point = self.points[self.index]
            self.canvas.create_oval(
                point.x - 6, point.y - 6, point.x + 6, point.y + 6, fill="red", outline="black", tags=f"h_{self.index}"
            )
            self.canvas.after(100, self._remove_highlight, self.index)
            self.index += 1
            self.canvas.after(self.get_speed(), self._animate)
        else:
            self.running = False

    def _remove_highlight(self, index):
        self.canvas.delete(f"h_{index}")


class UIController:
    """Класс для управления UI элементами, чтобы уменьшить количество атрибутов в PointVisualizer"""

    def __init__(self, parent):
        self.parent = parent
        self.vars = {
            "points_count": tk.IntVar(value=10),
            "line_x1": tk.IntVar(value=200),
            "line_y1": tk.IntVar(value=100),
            "line_x2": tk.IntVar(value=600),
            "line_y2": tk.IntVar(value=500),
            "speed_var": tk.IntVar(value=50),
        }
        self.widgets = {}

    def setup_ui(self, window):
        control_frame = ttk.Frame(window, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Панель точек
        ttk.Label(control_frame, text="Number of points:").grid(row=0, column=0, padx=5)
        ttk.Spinbox(control_frame, from_=1, to=50, textvariable=self.vars["points_count"], width=10).grid(
            row=0, column=1, padx=5
        )
        ttk.Button(control_frame, text="Generate Random Points", command=self.parent.generate_random_points).grid(
            row=0, column=2, padx=5
        )
        ttk.Button(control_frame, text="Clear Points", command=self.parent.clear_points).grid(row=0, column=3, padx=5)

        ttk.Separator(control_frame, orient="vertical").grid(row=0, column=4, rowspan=3, padx=10, sticky="ns")

        # Панель линии
        ttk.Label(control_frame, text="Line Point 1 (x,y):").grid(row=0, column=5, padx=5)
        ttk.Entry(control_frame, textvariable=self.vars["line_x1"], width=5).grid(row=0, column=6)
        ttk.Entry(control_frame, textvariable=self.vars["line_y1"], width=5).grid(row=0, column=7)

        ttk.Label(control_frame, text="Line Point 2 (x,y):").grid(row=1, column=5, padx=5)
        ttk.Entry(control_frame, textvariable=self.vars["line_x2"], width=5).grid(row=1, column=6)
        ttk.Entry(control_frame, textvariable=self.vars["line_y2"], width=5).grid(row=1, column=7)

        ttk.Button(control_frame, text="Draw Line", command=self.parent.draw_line).grid(
            row=0, column=8, rowspan=2, padx=5
        )
        ttk.Button(control_frame, text="Analyze Points", command=self.parent.analyze_points).grid(
            row=0, column=9, rowspan=2, padx=5
        )

        ttk.Separator(control_frame, orient="vertical").grid(row=0, column=10, rowspan=3, padx=10, sticky="ns")

        # Панель анимации
        ttk.Label(control_frame, text="Animation Speed (ms):").grid(row=0, column=11, padx=5)
        ttk.Scale(
            control_frame,
            from_=10,
            to=500,
            variable=self.vars["speed_var"],
            orient=tk.HORIZONTAL,
            length=100,
            command=self._update_speed,
        ).grid(row=0, column=12)
        self.widgets["speed_label"] = ttk.Label(control_frame, text="50ms")
        self.widgets["speed_label"].grid(row=0, column=13)

        self.widgets["animate_btn"] = ttk.Button(
            control_frame, text="Start Animation", command=self.parent.toggle_animation
        )
        self.widgets["animate_btn"].grid(row=1, column=11, columnspan=3)

        ttk.Button(control_frame, text="Screenshot", command=self.parent.take_screenshot).grid(
            row=2, column=0, columnspan=2
        )
        ttk.Button(control_frame, text="Exit", command=self.parent.on_closing).grid(row=2, column=2, columnspan=2)

        # Текстовое поле для результатов
        self.widgets["result_text"] = tk.Text(window, height=8, width=80)
        self.widgets["result_text"].pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        # Холст для рисования
        canvas = tk.Canvas(window, bg="white", width=800, height=500)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        return canvas

    def _update_speed(self, val):
        self.parent.speed = int(float(val))
        if "speed_label" in self.widgets:
            self.widgets["speed_label"].config(text=f"{self.parent.speed}ms")

    def update_animation_button(self, is_running):
        if "animate_btn" in self.widgets:
            self.widgets["animate_btn"].config(text="Stop Animation" if is_running else "Start Animation")

    def display_results(self, side1, side2, on_line):
        result_text = self.widgets["result_text"]
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Points on side +1: {len(side1)}\n")
        result_text.insert(tk.END, f"  {', '.join(side1) if side1 else 'None'}\n\n")
        result_text.insert(tk.END, f"Points on side -1: {len(side2)}\n")
        result_text.insert(tk.END, f"  {', '.join(side2) if side2 else 'None'}\n\n")
        result_text.insert(tk.END, f"Points on line: {len(on_line)}\n")
        result_text.insert(tk.END, f"  {', '.join(on_line) if on_line else 'None'}")


class PointVisualizer:
    """Теперь здесь ТОЛЬКО 6 атрибутов!"""

    def __init__(self, window):
        self.window = window  # 1
        self.points = []  # 2
        self.line = None  # 3
        self.speed = 50  # 4
        self.anim_manager = None  # 5
        self.ui = UIController(self)  # 6 - ВСЕ UI элементы в одном объекте!

        self._setup()

    def _setup(self):
        self.window.title("Point and Line Visualizer")
        self.window.geometry("900x700")

        self.canvas = self.ui.setup_ui(self.window)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _get_current_speed(self):
        return self.speed

    def generate_random_points(self):
        self.clear_points()
        count = self.ui.vars["points_count"].get()
        for _ in range(count):
            x = random.randint(50, 750)
            y = random.randint(50, 450)
            self.points.append(Point(x, y))
        self.draw_all()

    def clear_points(self):
        self.points = []
        self.draw_all()

    def draw_line(self):
        x1, y1 = self.ui.vars["line_x1"].get(), self.ui.vars["line_y1"].get()
        x2, y2 = self.ui.vars["line_x2"].get(), self.ui.vars["line_y2"].get()
        self.line = Line(Point(x1, y1), Point(x2, y2))
        self.draw_all()

    def draw_all(self):
        self.canvas.delete("all")
        LineDrawer.draw_line_with_labels(self.canvas, self.line)
        LineDrawer.draw_points(self.canvas, self.points, self.line)

    def on_canvas_click(self, event):
        self.points.append(Point(event.x, event.y))
        self.draw_all()

    def analyze_points(self):
        if not self.line:
            messagebox.showwarning("Warning", "Draw a line first!")
            return
        side1, side2, on_line = PointSideCalculator.classify_points(self.points, self.line)
        self.ui.display_results(side1, side2, on_line)
        self.draw_all()

    def toggle_animation(self):
        if not self.anim_manager:
            self.anim_manager = AnimationManager(self.canvas, self.points, self._get_current_speed)
        if not self.anim_manager.running:
            self.anim_manager.start()
            self.ui.update_animation_button(True)
        else:
            self.anim_manager.stop()
            self.ui.update_animation_button(False)

    def take_screenshot(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.ps"
        self.canvas.postscript(file=filename, colormode="color")
        messagebox.showinfo("Screenshot", f"Screenshot saved as {filename}")

    def on_closing(self):
        if self.anim_manager:
            self.anim_manager.stop()
        self.window.quit()
        self.window.destroy()


if __name__ == "__main__":
    app = tk.Tk()
    PointVisualizer(app)
    app.mainloop()
