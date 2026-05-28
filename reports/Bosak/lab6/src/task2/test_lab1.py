"""Tests for laboratory work 1 functions."""

import pytest
from .lab1_functions import sum_squares_negative, is_valid_brackets


def test_sum_squares_negative_normal():
    """Test with negative numbers."""
    assert sum_squares_negative([-1, -2, -3]) == 14


def test_sum_squares_negative_mixed():
    """Test with mixed positive and negative."""
    assert sum_squares_negative([1, -2, 3, -4, 5]) == 20


def test_sum_squares_negative_empty():
    """Test with empty list."""
    assert sum_squares_negative([]) == 0


def test_sum_squares_negative_no_negatives():
    """Test with only positive numbers."""
    assert sum_squares_negative([1, 2, 3]) == 0


def test_sum_squares_negative_type_error():
    """Test with non-list input."""
    with pytest.raises(TypeError, match="Input must be a list"):
        sum_squares_negative("not list")


def test_brackets_valid():
    """Test valid bracket sequences."""
    assert is_valid_brackets("()") is True
    assert is_valid_brackets("()[]{}") is True
    assert is_valid_brackets("([])") is True
    assert is_valid_brackets("({[]})") is True


def test_brackets_invalid():
    """Test invalid bracket sequences."""
    assert is_valid_brackets("(]") is False
    assert is_valid_brackets("([)]") is False
    assert is_valid_brackets("(") is False
    assert is_valid_brackets("]") is False


def test_brackets_empty():
    """Test empty string."""
    assert is_valid_brackets("") is True


def test_brackets_type_error():
    """Test with non-string input."""
    with pytest.raises(TypeError, match="Input must be a string"):
        is_valid_brackets(123)
