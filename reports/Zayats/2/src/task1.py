"""task1"""


class Rectangle:
    """Класс прямоугольника."""

    def __init__(self, a: float, b: float):
        """Создает прямоугольник со сторонами a и b."""
        self._a = a
        self._b = b

    @property
    def a(self):
        """Возвращает сторону a."""
        return self._a

    @a.setter
    def a(self, value):
        """Устанавливает сторону a."""
        self._a = value

    @property
    def b(self):
        """Возвращает сторону b."""
        return self._b

    @b.setter
    def b(self, value):
        """Устанавливает сторону b."""
        self._b = value

    def exists(self) -> bool:
        """Проверяет существование прямоугольника."""
        return self._a > 0 and self._b > 0

    def area(self) -> float:
        """Возвращает площадь прямоугольника."""
        return self._a * self._b if self.exists() else 0

    def perimeter(self) -> float:
        """Возвращает периметр прямоугольника."""
        return 2 * (self._a + self._b) if self.exists() else 0

    def is_square(self) -> bool:
        """Проверяет, является ли прямоугольник квадратом."""
        return self.exists() and self._a == self._b

    def __str__(self):
        """Возвращает строковое представление объекта."""
        return f"Прямоугольник: a={self._a}, b={self._b}"

    def __eq__(self, other):
        """Сравнивает два прямоугольника."""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self._a == other._a and self._b == other._b
