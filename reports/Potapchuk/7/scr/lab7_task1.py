import tkinter as tk
import random
import os
from PIL import ImageGrab


class MovingString:
    """Класс для управления отдельной движущейся строкой."""
    def __init__(self, canvas, text, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        # Случайная скорость и направление
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])
        self.id = self.canvas.create_text(
            random.randint(50, width - 50),
            random.randint(20, height - 20),
            text=text,
            fill=f"#{random.randint(0, 0xAAAAAA):06x}",
            font=("Arial", 12, "bold")
        )

    def move(self, speed_mult):
        """Метод для перемещения строки с проверкой границ."""
        self.canvas.move(self.id, self.vx * speed_mult, self.vy * speed_mult)
        pos = self.canvas.coords(self.id)

        # Отскок от левой/правой и верхней/нижней границ
        if pos[0] <= 10 or pos[0] >= self.width - 10:
            self.vx *= -1
        if pos[1] <= 10 or pos[1] >= self.height - 10:
            self.vy *= -1


class StringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная 7 - Задание 1")
        self.running = True

        self.ctrl = tk.Frame(root)
        self.ctrl.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Button(self.ctrl, text="Пауза/Старт", command=self.toggle).pack(side=tk.LEFT)
        tk.Button(self.ctrl, text="Скриншот", command=self.take_shot).pack(side=tk.LEFT, padx=5)

        tk.Label(self.ctrl, text=" Скорость:").pack(side=tk.LEFT)
        self.speed_val = tk.Scale(self.ctrl, from_=1, to=10, orient=tk.HORIZONTAL)
        self.speed_val.set(2)
        self.speed_val.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white", bd=2, relief="ridge")
        self.canvas.pack(padx=10, pady=10)

        data = ["Программирование", "Python 3.9", "БрГТУ", "Анита", "Visual Studio Code"]
        self.lines = [MovingString(self.canvas, txt, 600, 400) for txt in data]

        self.animate()

    def toggle(self):
        self.running = not self.running
        if self.running:
            self.animate()

    def take_shot(self):
        """Надежный захват окна приложения."""
        self.root.update()
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        
        path = os.path.join(os.getcwd(), "screenshot_task1.png")
        ImageGrab.grab(bbox=(x, y, x + w, y + h)).save(path)
        print(f"Сохранено: {path}")

    def animate(self):
        if self.running:
            s = self.speed_val.get() * 0.5
            for line in self.lines:
                line.move(s)
            self.root.after(30, self.animate)


if __name__ == "__main__":
    main_win = tk.Tk()
    app = StringApp(main_win)
    main_win.mainloop()
