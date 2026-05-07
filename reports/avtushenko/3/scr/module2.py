from abc import ABC, abstractmethod


# Команда
class Command(ABC):
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        pass


# Конкретные команды
class Add(Command):
    def execute(self, a, b):
        return a + b

    def get_symbol(self):
        return "+"


class Subtract(Command):
    def execute(self, a, b):
        return a - b

    def get_symbol(self):
        return "-"


class Multiply(Command):
    def execute(self, a, b):
        return a * b

    def get_symbol(self):
        return "×"


class Divide(Command):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Деление на ноль")
        return a / b

    def get_symbol(self):
        return "÷"


class Power(Command):
    def execute(self, a, b):
        return a**b

    def get_symbol(self):
        return "^"


class Modulo(Command):
    def execute(self, a, b):
        return a % b

    def get_symbol(self):
        return "%"


# Калькулятор с настраиваемыми кнопками
class Calculator:
    def __init__(self):
        self._custom_buttons = {}
        self._operations = {"+": Add(), "-": Subtract(), "×": Multiply(), "÷": Divide()}

    def assign_button(self, key: str, command: Command):
        self._custom_buttons[key] = command

    def press(self, key: str, a: float, b: float) -> float:
        # Фиксированные кнопки
        if key in self._operations:
            return self._operations[key].execute(a, b)
        # Настраиваемые кнопки
        if key in self._custom_buttons:
            return self._custom_buttons[key].execute(a, b)
        raise ValueError(f"Кнопка '{key}' не назначена")

    def show_buttons(self):
        print("Фиксированные:", " ".join(self._operations.keys()))
        print(
            "Настраиваемые:",
            (
                " ".join(
                    f"{k}({v.get_symbol()})" for k, v in self._custom_buttons.items()
                )
                if self._custom_buttons
                else "нет"
            ),
        )


# Демонстрация
if __name__ == "__main__":
    calc = Calculator()
    calc.show_buttons()

    # Фиксированные операции
    print(f"\n5 + 3 = {calc.press('+', 5, 3)}")
    print(f"10 ÷ 4 = {calc.press('÷', 10, 4)}")

    # Назначаем настраиваемые кнопки
    calc.assign_button("F1", Power())
    calc.assign_button("F2", Modulo())
    calc.show_buttons()

    # Используем настраиваемые
    print(f"\nF1: 2 ^ 10 = {calc.press('F1', 2, 10)}")
    print(f"F2: 17 % 5 = {calc.press('F2', 17, 5)}")

    # Переназначаем кнопку
    calc.assign_button("F1", Multiply())
    print(f"\nF1 переназначена: 7 × 8 = {calc.press('F1', 7, 8)}")
    calc.show_buttons()
