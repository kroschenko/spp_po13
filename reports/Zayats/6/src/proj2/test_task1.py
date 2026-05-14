"""Тесты 1 задания"""
# pylint: disable=import-error
from task1 import sum_squares_negative


def test_empty():
    """Тесты 1 задания"""
    assert sum_squares_negative([]) == 0


def test_only_positive():
    """Тесты 1 задания"""
    assert sum_squares_negative([1, 2, 3]) == 0


def test_negative_numbers():
    """Тесты 1 задания"""
    assert sum_squares_negative([-1, -2]) == 1 + 4


def test_mixed():
    """Тесты 1 задания"""
    assert sum_squares_negative([-3, 2, -4]) == 9 + 16
