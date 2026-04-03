
class Rectangle:

    def __init__(self, a: float, b: float):
        self._a = a
        self._b = b

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = value

    def exists(self) -> bool:
        return self._a > 0 and self._b > 0

    def area(self) -> float:
        return self._a * self._b if self.exists() else 0

    def perimeter(self) -> float:
        return 2 * (self._a + self._b) if self.exists() else 0

    def is_square(self) -> bool:
        return self.exists() and self._a == self._b

    def __str__(self):
        return f"Прямоугольник: a={self._a}, b={self._b}"

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self._a == other._a and self._b == other._b
    

height = float(input("Введите сторону a: "))
width = float(input("Введите сторону b: "))

rect = Rectangle(height, width)
print(rect)

if rect.exists():
    while True:
        s = input("""1. Площадь
2. Периметр
3. Квадрат ли это?
""")
        
        if s == "":
            break
        
        if s == "1":
            print("Площадь:", rect.area())
        elif s == "2":
            print("Периметр:", rect.perimeter())
        elif s == "3":
            print("Это квадрат:", rect.is_square())
        else:
            print("Неверный ввод")
else:
    print("Такой прямоугольник не существует")
