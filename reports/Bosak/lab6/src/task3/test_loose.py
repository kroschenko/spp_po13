"""Tests for loose function."""

import pytest
from .loose import loose


def test_both_none():
    """Test both arguments None."""
    with pytest.raises(TypeError):
        loose(None, None)


def test_first_none_second_string():
    """Test first None, second string."""
    assert loose(None, "abc") is None


def test_first_string_second_none():
    """Test first string, second None."""
    assert loose("hello", None) == "hello"


def test_empty_string():
    """Test empty first string."""
    assert loose("", "abc") == ""


def test_empty_remove():
    """Test empty remove string."""
    assert loose("hello", "") == "hello"


def test_normal_case_remove_hl():
    """Test removing 'h' and 'l' from ' hello '."""
    assert loose(" hello ", "hl") == "eo"


def test_normal_case_remove_le():
    """Test removing 'l' and 'e' from ' hello '."""
    assert loose(" hello ", "le") == "ho"


def test_no_chars_to_remove():
    """Test removing characters not in string."""
    assert loose("hello", "xyz") == "hello"


def test_all_chars_removed():
    """Test removing all characters."""
    assert loose("abc", "abc") == ""


def test_non_string_first():
    """Test first argument not a string."""
    with pytest.raises(TypeError, match="Both arguments must be strings"):
        loose(123, "abc")


def test_non_string_second():
    """Test second argument not a string."""
    with pytest.raises(TypeError, match="Both arguments must be strings"):
        loose("abc", 123)
