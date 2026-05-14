"""task1"""
# pylint: disable=duplicate-code
def parse_numbers(inputs: list[str]) -> list[int]:
    """Преобразует строки в числа, игнорируя неверные."""
    numbers = []

    for user_input in inputs:
        if user_input == "":
            break
        try:
            numbers.append(int(user_input))
        except ValueError:
            pass

    return numbers


def sum_squares_negative(numbers: list[int]) -> int:
    """Сумма квадратов отрицательных чисел."""
    return sum(x ** 2 for x in numbers if x < 0)


def run():
    """Запуск программы."""
    numbers = []

    print("Вводите числа (Enter для завершения):")

    while True:
        user_input = input("Число: ")

        if user_input == "":
            break

        try:
            numbers.append(int(user_input))
        except ValueError:
            print("Введите целое число!")

    result = sum_squares_negative(numbers)

    print("Числа:", numbers)
    print("Сумма квадратов отрицательных чисел:", result)


if __name__ == "__main__":
    run()
