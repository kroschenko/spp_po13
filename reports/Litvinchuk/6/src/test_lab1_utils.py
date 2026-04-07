"""Tests for lab1 utility functions."""

import pytest

from src.lab1_utils import is_palindrome, rep


def test_rep_normal_case():
    """Test rep with standard positive step."""
    assert rep(1, 5, 1) == [1, 2, 3, 4, 5]


def test_rep_with_step_two():
    """Test rep with step equal to two."""
    assert rep(1, 5, 2) == [1, 3, 5]


def test_rep_single_value():
    """Test rep when start and end are equal."""
    assert rep(3, 3, 1) == [3]


def test_rep_empty_when_start_greater_than_end():
    """Test rep when range is empty."""
    assert not rep(5, 1, 1)


def test_rep_zero_step_raises():
    """Test rep with zero step."""
    with pytest.raises(ValueError, match="Step cannot be zero"):
        rep(1, 5, 0)


def test_is_palindrome_simple_true():
    """Test simple palindrome."""
    assert is_palindrome("abba") is True


def test_is_palindrome_simple_false():
    """Test simple non-palindrome."""
    assert is_palindrome("hello") is False


def test_is_palindrome_mixed_case():
    """Test palindrome with mixed case."""
    assert is_palindrome("AbBa") is True


def test_is_palindrome_with_spaces_and_punctuation():
    """Test palindrome with punctuation and spaces."""
    assert is_palindrome("A man, a plan, a canal: Panama!") is True


def test_is_palindrome_empty_string():
    """Test empty string palindrome."""
    assert is_palindrome("") is True


def test_is_palindrome_digits():
    """Test numeric palindrome."""
    assert is_palindrome("12321") is True


def test_is_palindrome_alphanumeric_false():
    """Test alphanumeric non-palindrome."""
    assert is_palindrome("abc123") is False
