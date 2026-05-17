import turtle
import tkinter as tk
from tkinter import ttk, colorchooser
import math
from dataclasses import dataclass


@dataclass
class FractalParams:
    level: tk.IntVar = None
    length: tk.IntVar = None
    speed: tk.IntVar = None
    color: str = "#FF0000"
    bg_color: str = "#FFFFFF"
    pen_size: tk.IntVar = None

    def __post_init__(self):
        if self.level is None:
            self.level = tk.IntVar(value=1)
        if self.length is None:
            self.length = tk.IntVar(value=150)
        if self.speed is None:
            self.speed = tk.IntVar(value=5)
        if self.pen_size is None:
            self.pen_size = tk.IntVar(value=2)

    def get_all_params(self):
        return (self.level.get(), self.length.get(), self.speed.get(),
                self.color, self.bg_color, self.pen_size.get())


class UIControls:
    def __init__(self, parent, params):
        self.parent = parent
        self.params = params
        self.level_label = None
        self.length_label = None
        self.speed_label = None
        self.color_preview = None

    def create_level_control(self):
        ttk.Label(self.parent, text="Recursion level (0-4):").pack(anchor=tk.W)
        level_frame = ttk.Frame(self.parent)
        level_frame.pack(fill=tk.X, pady=(0, 10))
        level_scale = ttk.Scale(
            level_frame, from_=0, to=4, variable=self.params.level, command=self._update_level_label
        )
        level_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.level_label = ttk.Label(level_frame, text="1", width=5, font=("Arial", 10, "bold"))
        self.level_label.pack(side=tk.RIGHT, padx=(5, 0))

    def create_length_control(self):
        ttk.Label(self.parent, text="Side length (50-200):").pack(anchor=tk.W)
        length_frame = ttk.Frame(self.parent)
        length_frame.pack(fill=tk.X, pady=(0, 10))
        length_scale = ttk.Scale(
            length_frame, from_=50, to=200, variable=self.params.length, command=self._update_length_label
        )
        length_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.length_label = ttk.Label(length_frame, text="150", width=5, font=("Arial", 10, "bold"))
        self.length_label.pack(side=tk.RIGHT, padx=(5, 0))

    def create_speed_control(self):
        ttk.Label(self.parent, text="Speed (0-10):").pack(anchor=tk.W)
        speed_frame = ttk.Frame(self.parent)
        speed_frame.pack(fill=tk.X, pady=(0, 10))
        speed_scale = ttk.Scale(
            speed_frame, from_=0, to=10, variable=self.params.speed, command=self._update_speed_label
        )
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.speed_label = ttk.Label(speed_frame, text="5", width=5)
        self.speed_label.pack(side=tk.RIGHT, padx=(5, 0))

    def create_pen_control(self):
        ttk.Label(self.parent, text="Pen size (1-5):").pack(anchor=tk.W)
        pen_frame = ttk.Frame(self.parent)
        pen_frame.pack(fill=tk.X, pady=(0, 10))
        pen_scale = ttk.Scale(pen_frame, from_=1, to=5, variable=self.params.pen_size)
        pen_scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def create_color_controls(self, color_callback, bg_callback):
        ttk.Label(self.parent, text="Colors:").pack(anchor=tk.W, pady=(5, 0))
        color_frame = ttk.Frame(self.parent)
        color_frame.pack(fill=tk.X, pady=5)

        ttk.Button(color_frame, text="Line color", command=color_callback).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(color_frame, text="Background color", command=bg_callback).pack(side=tk.LEFT)

        self.color_preview = tk.Canvas(color_frame, width=30, height=25, bg=self.params.color, highlightthickness=1)
        self.color_preview.pack(side=tk.RIGHT, padx=5)

    def _update_level_label(self, _=None):
        level = int(self.params.level.get())
        self.level_label.config(text=str(level))

    def _update_length_label(self, _=None):
        self.length_label.config(text=str(int(self.params.length.get())))

    def _update_speed_label(self, _=None):
        self.speed_label.config(text=str(int(self.params.speed.get())))


class FractalRenderer:
    def __init__(self, params):
        self.params = params
        self.turtle_window = None
        self.canvas = None
        self.turtle_obj = None
        self.is_drawing = False

    def close_window(self):
        if self.turtle_window and self.turtle_window.winfo_exists():
            self.is_drawing = False
            self.turtle_window.destroy()
            self.turtle_window = None
            self.canvas = None
            self.turtle_obj = None

    def test_drawing(self, root, progress_callback):
        self.close_window()

        self.turtle_window = tk.Toplevel(root)
        self.turtle_window.title("Test Drawing")
        self.turtle_window.geometry("600x600")
        self.turtle_window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.canvas = tk.Canvas(self.turtle_window, bg="white", highlightthickness=1)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.turtle_window.update()

        self.turtle_obj = turtle.RawTurtle(self.canvas)

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        self.turtle_obj.screen.setworldcoordinates(0, canvas_height, canvas_width, 0)

        self.turtle_obj.speed(3)
        self.turtle_obj.pencolor("red")
        self.turtle_obj.pensize(3)
        self.turtle_obj.penup()

        square_size = 100
        start_x = (canvas_width - square_size) / 2
        start_y = (canvas_height - square_size) / 2

        self.turtle_obj.goto(start_x, start_y)
        self.turtle_obj.pendown()

        for _ in range(4):
            self.turtle_obj.forward(square_size)
            self.turtle_obj.right(90)

        self.turtle_obj.hideturtle()
        progress_callback("Test square drawn")

        self.canvas.create_text(
            canvas_width // 2, 30, text="If you see a red square - drawing works", fill="blue", font=("Arial", 10)
        )

    def _draw_segment(self, length, level):
        if level == 0 or not self.is_drawing:
            if self.is_drawing and self.turtle_obj:
                self.turtle_obj.forward(length)
            return

        new_len = length / 4.0

        if self.is_drawing:
            self._draw_segment(new_len, level - 1)
            if self.is_drawing:
                self.turtle_obj.left(90)
                self._draw_segment(new_len, level - 1)

            if self.is_drawing:
                self.turtle_obj.right(90)
                self._draw_segment(new_len, level - 1)

            if self.is_drawing:
                self.turtle_obj.right(90)
                self._draw_segment(new_len, level - 1)

            if self.is_drawing:
                self._draw_segment(new_len, level - 1)

            if self.is_drawing:
                self.turtle_obj.left(90)
                self._draw_segment(new_len, level - 1)

            if self.is_drawing:
                self.turtle_obj.left(90)
                self._draw_segment(new_len, level - 1)

            if self.is_drawing:
                self.turtle_obj.right(90)
                self._draw_segment(new_len, level - 1)

    def _setup_window(self, root, level, bg_color):
        self.turtle_window = tk.Toplevel(root)
        self.turtle_window.title(f"Minkowski Island (level {level})")
        self.turtle_window.geometry("700x700")
        self.turtle_window.protocol("WM_DELETE_WINDOW", self.close_window)

        self.canvas = tk.Canvas(self.turtle_window, bg=bg_color, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.turtle_window.update()

    def _setup_turtle(self, speed, color, pen_size):
        self.turtle_obj = turtle.RawTurtle(self.canvas)
        self.turtle_obj.speed(speed)
        self.turtle_obj.pencolor(color)
        self.turtle_obj.pensize(pen_size)
        self.turtle_obj.penup()

    def _setup_coordinates(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        self.turtle_obj.screen.setworldcoordinates(0, canvas_height, canvas_width, 0)
        return canvas_width, canvas_height

    def _calculate_start_position(self, level, side_length, canvas_width, canvas_height):
        if level == 0:
            fractal_size = side_length
        else:
            fractal_size = side_length * (1.5**level)

        start_x = (canvas_width - fractal_size) / 2
        start_y = (canvas_height - fractal_size) / 2
        return start_x, start_y, fractal_size

    def _draw_fractal_sides(self, side_length, level, progress_callback, root):
        for side in range(4):
            if not self.is_drawing:
                break
            self._draw_segment(side_length, level)
            if not self.is_drawing:
                break
            self.turtle_obj.right(90)
            progress_callback(f"Side {side + 1}/4")
            root.update()

    def draw_fractal(self, root, progress_callback, info_callback):
        self.close_window()

        level = self.params.level.get()
        side_length = self.params.length.get()

        self._setup_window(root, level, self.params.bg_color)
        self._setup_turtle(self.params.speed.get(), self.params.color, self.params.pen_size.get())
        canvas_width, canvas_height = self._setup_coordinates()
        start_x, start_y, fractal_size = self._calculate_start_position(level, side_length, canvas_width, canvas_height)

        self.turtle_obj.goto(start_x, start_y)

        info_text = f"Level: {level} | Side length: {side_length}px | Size: {fractal_size:.0f}px"
        self.canvas.create_text(canvas_width // 2, 20, text=info_text, fill="gray", font=("Arial", 10))

        self.turtle_obj.pendown()
        self.is_drawing = True
        progress_callback(f"Drawing level {level}...")
        root.update()

        try:
            self._draw_fractal_sides(side_length, level, progress_callback, root)
            self.turtle_obj.hideturtle()
            progress_callback("Fractal ready")
            info_callback(level, side_length)
        except (RuntimeError, AttributeError):
            progress_callback("Error during drawing")
        finally:
            self.is_drawing = False


class MinkowskiIslandApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fractal 'Minkowski Island'")
        self.root.geometry("400x700")
        self.root.resizable(False, False)

        self.params = FractalParams()
        self.renderer = FractalRenderer(self.params)
        self.info_text = None
        self.progress_var = None
        self.color_preview = None

        self._setup_ui()

    def _setup_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(main_frame, text="Minkowski Island", font=("Arial", 18, "bold"))
        title.pack(pady=(0, 15))

        controls = UIControls(main_frame, self.params)

        controls.create_level_control()
        controls.create_length_control()
        controls.create_speed_control()
        controls.create_pen_control()
        controls.create_color_controls(self._choose_color, self._choose_bg_color)

        self.color_preview = controls.color_preview

        self._add_buttons(main_frame)
        self._add_info_panel(main_frame)

        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(main_frame, textvariable=self.progress_var, font=("Arial", 9), foreground="green")
        progress_label.pack(pady=(5, 0))

        hint = ttk.Label(
            main_frame, text="Hint: start with level 1 and length 150", font=("Arial", 8), foreground="blue"
        )
        hint.pack(pady=(5, 0))

    def _add_buttons(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, pady=(10, 5))

        ttk.Button(btn_frame, text="DRAW FRACTAL", command=self.draw_fractal).pack(fill=tk.X, pady=2)

        ttk.Button(btn_frame, text="TEST (square)", command=self._test_drawing).pack(fill=tk.X, pady=2)

        ttk.Button(btn_frame, text="CLOSE WINDOW", command=self._close_window).pack(fill=tk.X, pady=2)

    def _add_info_panel(self, parent):
        info_frame = ttk.LabelFrame(parent, text="Information", padding=5)
        info_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        self.info_text = tk.Text(info_frame, height=10, width=40, font=("Courier", 9))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        self._update_info(1, 150)

    def _choose_color(self):
        color = colorchooser.askcolor(title="Choose line color", color=self.params.color)
        if color[1]:
            self.params.color = color[1]
            self.color_preview.config(bg=self.params.color)

    def _choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose background color", color=self.params.bg_color)
        if color[1]:
            self.params.bg_color = color[1]
            if self.renderer.canvas and self.renderer.canvas.winfo_exists():
                self.renderer.canvas.config(bg=self.params.bg_color)

    def _close_window(self):
        self.renderer.close_window()
        self.progress_var.set("Window closed")

    def _test_drawing(self):
        self.renderer.test_drawing(self.root, self._update_progress)

    def draw_fractal(self):
        self.renderer.draw_fractal(self.root, self._update_progress, self._update_info)

    def _update_progress(self, message):
        self.progress_var.set(message)
        self.root.update()

    def _update_info(self, level, length):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)

        if level == 0:
            segments = 4
            perimeter = length * 4
            fractal_size = length
        else:
            segments = 4 * (8**level)
            perimeter = length * 4 * ((4 / 3) ** level)
            fractal_size = length * (1.5**level)

        info = (
            f"MINKOWSKI ISLAND\n"
            f"{'=' * 35}\n"
            f"Level: {level}\n"
            f"Side length: {length} px\n"
            f"Size: {fractal_size:.0f} px\n"
            f"Pen size: {self.params.pen_size.get()}\n"
            f"\nStatistics:\n"
            f"Segments: {segments:,}\n"
            f"Perimeter: {perimeter:.0f} px\n"
            f"\nDimension:\n"
            f"D = log(8)/log(4)\n"
            f"D = {math.log(8) / math.log(4):.3f}\n"
            f"\nFractal is a curve\n"
            f"of infinite length\n"
            f"in a bounded area"
        )

        self.info_text.insert("1.0", info)
        self.info_text.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = MinkowskiIslandApp(root)
    app.run()


if __name__ == "__main__":
    main()
