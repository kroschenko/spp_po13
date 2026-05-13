"""Функции из лабораторной работы 1."""


def parse_numbers(text):
    """Преобразует строку в список целых чисел."""
    if not text.split():
        raise ValueError("Empty input")

    return [int(number) for number in text.split()]


def calculate_median(numbers):
    """Вычисляет медиану списка чисел."""
    if not numbers:
        raise ValueError("Empty list")

    sorted_numbers = sorted(numbers)
    middle = len(sorted_numbers) // 2

    if len(sorted_numbers) % 2 == 1:
        return sorted_numbers[middle]

    return (sorted_numbers[middle - 1] + sorted_numbers[middle]) / 2


def parse_digits(text):
    """Преобразует строку в список цифр."""
    if not text.split():
        raise ValueError("Empty input")

    digits = [int(digit) for digit in text.split()]

    if any(digit < 0 or digit > 9 for digit in digits):
        raise ValueError("Invalid digit")

    if len(digits) > 1 and digits[0] == 0:
        raise ValueError("Leading zero")

    return digits


def plus_one(digits):
    """Увеличивает число, представленное списком цифр, на единицу."""
    if not digits:
        raise ValueError("Empty list")

    result = digits[:]
    index = len(result) - 1

    while index >= 0:
        if result[index] < 9:
            result[index] += 1
            return result

        result[index] = 0
        index -= 1

    return [1] + result
