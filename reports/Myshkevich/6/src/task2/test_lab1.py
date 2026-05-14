"""Тесты для первой лабораторной работы."""
import pytest
from lab1_functions import (
    shuffle_numbers,
    find_majority_element,
    parse_numbers,
    process_numbers
)


# ==================== ТЕСТЫ ДЛЯ SHUFFLE_NUMBERS ====================
def test_shuffle_numbers_basic():
    """Проверка перемешивания чисел."""
    numbers = [1, 2, 3, 4, 5]
    shuffled = shuffle_numbers(numbers)

    # Проверяем, что длина не изменилась
    assert len(shuffled) == len(numbers)

    # Проверяем, что все элементы остались
    assert sorted(shuffled) == sorted(numbers)


def test_shuffle_numbers_empty():
    """Проверка перемешивания пустого списка."""
    assert not shuffle_numbers([])


def test_shuffle_numbers_single():
    """Проверка перемешивания списка из одного элемента."""
    numbers = [42]
    assert shuffle_numbers(numbers) == [42]


def test_shuffle_numbers_does_not_modify_original():
    """Проверка, что исходный список не изменяется."""
    original = [1, 2, 3, 4, 5]
    copy = original.copy()
    shuffle_numbers(original)
    assert original == copy


# ==================== ТЕСТЫ ДЛЯ FIND_MAJORITY_ELEMENT ====================
def test_majority_element_exists_odd():
    """Проверка: элемент большинства существует (нечетное количество)."""
    arr = [3, 3, 4, 2, 3, 3, 3]
    assert find_majority_element(arr) == 3


def test_majority_element_exists_even():
    """Проверка: элемент большинства существует (четное количество)."""
    arr = [1, 1, 1, 2, 2, 1]
    assert find_majority_element(arr) == 1


def test_majority_element_not_exists():
    """Проверка: элемент большинства не существует."""
    arr = [1, 2, 3, 4, 5]
    assert find_majority_element(arr) is None


def test_majority_element_tie():
    """Проверка: голоса поровну (элемента большинства нет)."""
    arr = [1, 1, 2, 2]
    assert find_majority_element(arr) is None


def test_majority_element_single():
    """Проверка: список из одного элемента."""
    arr = [42]
    assert find_majority_element(arr) == 42


def test_majority_element_two_same():
    """Проверка: два одинаковых элемента."""
    arr = [5, 5]
    assert find_majority_element(arr) == 5


def test_majority_element_two_different():
    """Проверка: два разных элемента (элемента большинства нет)."""
    arr = [1, 2]
    assert find_majority_element(arr) is None


def test_majority_element_empty():
    """Проверка: пустой список."""
    assert find_majority_element([]) is None


def test_majority_element_all_same():
    """Проверка: все элементы одинаковые."""
    arr = [7, 7, 7, 7, 7]
    assert find_majority_element(arr) == 7


def test_majority_element_large_numbers():
    """Проверка: большие числа."""
    arr = [1000000, 1000000, 999999, 1000000]
    assert find_majority_element(arr) == 1000000


def test_majority_element_negative():
    """Проверка: отрицательные числа."""
    arr = [-1, -1, -2, -1, -1]
    assert find_majority_element(arr) == -1


def test_majority_element_mixed():
    """Проверка: смешанные положительные и отрицательные."""
    arr = [1, -1, 1, -1, 1, 1, -1]
    assert find_majority_element(arr) == 1


# ==================== ТЕСТЫ ДЛЯ PARSE_NUMBERS ====================
def test_parse_numbers_valid():
    """Проверка парсинга корректной строки."""
    assert parse_numbers("1 2 3 4 5") == [1, 2, 3, 4, 5]


def test_parse_numbers_single():
    """Проверка парсинга одного числа."""
    assert parse_numbers("42") == [42]


def test_parse_numbers_empty():
    """Проверка парсинга пустой строки."""
    assert not parse_numbers("")
    assert not parse_numbers("   ")


def test_parse_numbers_with_spaces():
    """Проверка парсинга с лишними пробелами."""
    assert parse_numbers("  1   2   3  ") == [1, 2, 3]


def test_parse_numbers_negative():
    """Проверка парсинга отрицательных чисел."""
    assert parse_numbers("-1 -2 -3") == [-1, -2, -3]


def test_parse_numbers_mixed():
    """Проверка парсинга смешанных чисел."""
    assert parse_numbers("10 -20 30 -40") == [10, -20, 30, -40]


def test_parse_numbers_invalid():
    """Проверка: выброс ошибки при нечисловом значении."""
    with pytest.raises(ValueError, match="не является целым числом"):
        parse_numbers("1 2 a 4")


def test_parse_numbers_invalid_with_text():
    """Проверка: выброс ошибки при тексте."""
    with pytest.raises(ValueError):
        parse_numbers("hello world")


# ==================== ТЕСТЫ ДЛЯ PROCESS_NUMBERS ====================
def test_process_numbers_normal():
    """Проверка обработки обычного ввода."""
    result = process_numbers("1 2 3 3 3")
    assert result["numbers"] == [1, 2, 3, 3, 3]
    assert result["majority_element"] == 3
    assert "Элемент большинства: 3" in result["message"]


def test_process_numbers_no_majority():
    """Проверка обработки без элемента большинства."""
    result = process_numbers("1 2 3 4 5")
    assert result["majority_element"] is None
    assert result["message"] == "Элемент большинства не найден"


def test_process_numbers_empty():
    """Проверка обработки пустого ввода."""
    result = process_numbers("")
    assert not result["numbers"]
    assert not result["shuffled"]
    assert result["majority_element"] is None
    assert result["message"] == "Список пуст"


def test_process_numbers_single():
    """Проверка обработки одного числа."""
    result = process_numbers("42")
    assert result["numbers"] == [42]
    assert result["majority_element"] == 42


def test_process_numbers_shuffled():
    """Проверка, что shuffled список содержит те же элементы."""
    result = process_numbers("1 2 3 4 5")
    assert sorted(result["shuffled"]) == sorted(result["numbers"])


def test_process_numbers_invalid():
    """Проверка: выброс ошибки при неверном вводе."""
    with pytest.raises(ValueError, match="не является целым числом"):
        process_numbers("1 2 a 4")


# ==================== ДОПОЛНИТЕЛЬНЫЕ ГРАНИЧНЫЕ ТЕСТЫ ====================
def test_majority_element_one_more_than_half():
    """Граничный случай: ровно на 1 больше половины."""
    arr = [1, 1, 1, 2, 3]  # 3 > 5/2 = 2.5
    assert find_majority_element(arr) == 1


def test_majority_element_exactly_half():
    """Граничный случай: ровно половина (не элемент большинства)."""
    arr = [1, 1, 2, 2]  # 2 == 4/2
    assert find_majority_element(arr) is None


def test_majority_element_max_size():
    """Проверка на большом количестве элементов."""
    n = 100001
    arr = [1] * (n // 2 + 1) + [2] * (n // 2)
    assert find_majority_element(arr) == 1


def test_parse_numbers_max_int():
    """Проверка парсинга максимального целого числа."""
    assert parse_numbers("2147483647") == [2147483647]
    assert parse_numbers("-2147483648") == [-2147483648]
