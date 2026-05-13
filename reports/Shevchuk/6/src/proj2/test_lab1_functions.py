# pylint: disable=import-error

"""Тесты к функциям из лабораторной работы 1."""

import pytest

from lab1_functions import calculate_median, parse_digits, parse_numbers, plus_one


def test_parse_numbers():
    """Проверяет преобразование строки в список чисел."""
    assert parse_numbers("1 2 3") == [1, 2, 3]


def test_parse_numbers_empty():
    """Проверяет ошибку при пустом вводе."""
    with pytest.raises(ValueError):
        parse_numbers("")


def test_parse_numbers_invalid():
    """Проверяет ошибку при некорректном числе."""
    with pytest.raises(ValueError):
        parse_numbers("1 a 3")


@pytest.mark.parametrize(
    ("numbers", "expected"),
    [
        ([1, 2, 3], 2),
        ([1, 2, 3, 4], 2.5),
        ([5], 5),
        ([-3, -1, -2], -2),
    ],
)
def test_calculate_median(numbers, expected):
    """Проверяет вычисление медианы."""
    assert calculate_median(numbers) == expected


def test_calculate_median_empty():
    """Проверяет ошибку при пустом списке."""
    with pytest.raises(ValueError):
        calculate_median([])


def test_parse_digits():
    """Проверяет преобразование строки в список цифр."""
    assert parse_digits("1 2 3") == [1, 2, 3]


@pytest.mark.parametrize("text", ["", "1 10 3", "1 -1 3", "0 1 2"])
def test_parse_digits_invalid(text):
    """Проверяет ошибки при неверном вводе цифр."""
    with pytest.raises(ValueError):
        parse_digits(text)


@pytest.mark.parametrize(
    ("digits", "expected"),
    [
        ([1, 2, 3], [1, 2, 4]),
        ([1, 2, 9], [1, 3, 0]),
        ([9], [1, 0]),
        ([9, 9, 9], [1, 0, 0, 0]),
    ],
)
def test_plus_one(digits, expected):
    """Проверяет увеличение числа на единицу."""
    assert plus_one(digits) == expected


def test_plus_one_empty():
    """Проверяет ошибку при пустом списке."""
    with pytest.raises(ValueError):
        plus_one([])
