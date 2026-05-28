"""Module for Rectangle class."""


class Rectangle:
    """Rectangle with sides a and b."""

    def __init__(self, side_a, side_b):
        self.side_a = side_a
        self.side_b = side_b

    def area(self):
        """Calculate area."""
        return self.side_a * self.side_b

    def perimeter(self):
        """Calculate perimeter."""
        return 2 * (self.side_a + self.side_b)

    def is_square(self):
        """Check if rectangle is square."""
        return self.side_a == self.side_b

    def exists(self):
        """Check if rectangle exists."""
        return self.side_a > 0 and self.side_b > 0

    def __str__(self):
        return f"Rectangle({self.side_a}, {self.side_b})"

    def __eq__(self, other):
        return self.area() == other.area()


def main():
    """Read input and demonstrate rectangle."""
    a = float(input("Side a: "))
    b = float(input("Side b: "))
    rect = Rectangle(a, b)
    print(rect)
    print(f"Area: {rect.area()}")
    print(f"Perimeter: {rect.perimeter()}")
    print(f"Is square: {rect.is_square()}")
    print(f"Exists: {rect.exists()}")


if __name__ == "__main__":
    main()
