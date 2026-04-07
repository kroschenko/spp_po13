import pytest
from lab1_utils import rep, is_palindrome


def test_rep_normal_case():
    assert rep(1, 5, 1) == [1, 2, 3, 4, 5]


def test_rep_with_step_two():
    assert rep(1, 5, 2) == [1, 3, 5]


def test_rep_single_value():
    assert rep(3, 3, 1) == [3]


def test_rep_empty_when_start_greater_than_end():
    assert rep(5, 1, 1) == []


def test_rep_zero_step_raises():
    with pytest.raises(ValueError, match="Step cannot be zero"):
        rep(1, 5, 0)


def test_is_palindrome_simple_true():
    assert is_palindrome("abba") is True


def test_is_palindrome_simple_false():
    assert is_palindrome("hello") is False


def test_is_palindrome_mixed_case():
    assert is_palindrome("AbBa") is True


def test_is_palindrome_with_spaces_and_punctuation():
    assert is_palindrome("A man, a plan, a canal: Panama!") is True


def test_is_palindrome_empty_string():
    assert is_palindrome("") is True


def test_is_palindrome_digits():
    assert is_palindrome("12321") is True


def test_is_palindrome_alphanumeric_false():
    assert is_palindrome("abc123") is False
