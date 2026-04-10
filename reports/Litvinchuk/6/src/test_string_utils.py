"""Tests for string utility functions."""

import pytest

from src.string_utils import keep


def test_keep_none_none():
    """Test keep with both arguments equal to None."""
    with pytest.raises(TypeError):
        keep(None, None)


def test_keep_none_pattern():
    """Test keep with None string and valid pattern."""
    assert keep(None, "abc") is None


def test_keep_empty_string():
    """Test keep with empty string."""
    assert keep("", "abc") == ""


def test_keep_pattern_none():
    """Test keep with None pattern."""
    assert keep("hello", None) == ""


def test_keep_pattern_empty():
    """Test keep with empty pattern."""
    assert keep("hello", "") == ""


def test_keep_hl():
    """Test keep with pattern hl."""
    assert keep(" hello ", "hl") == " hll "


def test_keep_le():
    """Test keep with pattern le."""
    assert keep(" hello ", "le") == " ell "


def test_keep_no_matches():
    """Test keep when there are no matching characters."""
    assert keep("abc", "xyz") == ""


def test_keep_all_matches():
    """Test keep when all characters match."""
    assert keep("abc", "abc") == "abc"


def test_keep_repeated_chars():
    """Test keep with repeated matching characters."""
    assert keep("hello world", "lo") == "llo ol"
