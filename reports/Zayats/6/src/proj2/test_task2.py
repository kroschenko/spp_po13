"""Тесты 2 задания"""
# pylint: disable=import-error
from task2 import is_brackets_correct


def test_empty():
    """Тесты 2 задания"""
    assert is_brackets_correct("") is True


def test_simple_ok():
    """Тесты 2 задания"""
    assert is_brackets_correct("()") is True


def test_nested():
    """Тесты 2 задания"""
    assert is_brackets_correct("([{}])") is True


def test_wrong_order():
    """Тесты 2 задания"""
    assert is_brackets_correct("(]") is False


def test_missing_close():
    """Тесты 2 задания"""
    assert is_brackets_correct("(((") is False


def test_extra_close():
    """Тесты 2 задания"""
    assert is_brackets_correct("())") is False


def test_text():
    """Тесты 2 задания"""
    assert is_brackets_correct("a(b)c") is True
