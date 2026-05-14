"""Функции из первой лабораторной работы."""
import random
from collections import Counter
from typing import List, Optional


def shuffle_numbers(numbers: List[int]) -> List[int]:
    """
    Перемешивает список чисел в случайном порядке.

    Args:
        numbers: Список целых чисел

    Returns:
        Новый перемешанный список
    """
    shuffled = numbers.copy()
    random.shuffle(shuffled)
    return shuffled


def find_majority_element(arr: List[int]) -> Optional[int]:
    """
    Находит элемент большинства (встречается более n/2 раз).

    Args:
        arr: Список целых чисел

    Returns:
        Элемент большинства или None, если его нет
    """
    if not arr:
        return None

    counts = Counter(arr)
    n = len(arr)

    for num, freq in counts.items():
        if freq > n // 2:
            return num

    return None


def parse_numbers(input_str: str) -> List[int]:
    """
    Преобразует строку с числами через пробел в список целых чисел.

    Args:
        input_str: Строка с числами, разделенными пробелами

    Returns:
        Список целых чисел

    Raises:
        ValueError: Если строка содержит нечисловые значения
    """
    if not input_str.strip():
        return []

    parts = input_str.strip().split()
    result = []
    for part in parts:
        try:
            result.append(int(part))
        except ValueError as e:
            raise ValueError(f"'{part}' не является целым числом") from e
    return result


def process_numbers(input_str: str) -> dict:
    """
    Обрабатывает ввод чисел: парсит, перемешивает и находит элемент большинства.

    Args:
        input_str: Строка с числами через пробел

    Returns:
        Словарь с результатами обработки
    """
    numbers = parse_numbers(input_str)

    if not numbers:
        return {
            "numbers": [],
            "shuffled": [],
            "majority_element": None,
            "message": "Список пуст"
        }

    shuffled = shuffle_numbers(numbers)
    majority = find_majority_element(numbers)

    return {
        "numbers": numbers,
        "shuffled": shuffled,
        "majority_element": majority,
        "message": f"Элемент большинства: {majority}" if majority else "Элемент большинства не найден"
    }


def main():
    """Главная функция для интерактивного режима."""
    # Первая часть: перемешивание чисел
    input_str = input("Введите числа через пробел: ")
    numbers = parse_numbers(input_str)
    shuffled = shuffle_numbers(numbers)
    print("Числа в случайном порядке:", *shuffled)

    # Вторая часть: поиск элемента большинства
    input_str = input("Введите числа через пробел: ")
    nums = parse_numbers(input_str)
    result = find_majority_element(nums)

    if result is not None:
        print(f"Элемент большинства: {result}")
    else:
        print("Элемент большинства не найден")


if __name__ == "__main__":
    main()
