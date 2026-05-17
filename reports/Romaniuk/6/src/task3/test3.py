"""Tests for hamming_distance function."""
import pytest
from task3 import hamming_distance


class TestHammingDistance:
    def test_both_none(self):
        with pytest.raises(TypeError):
            hamming_distance(None, None)

    def test_first_none(self):
        assert hamming_distance(None, "abc") == -1

    def test_second_none(self):
        assert hamming_distance("abc", None) == -1

    def test_not_string_first(self):
        assert hamming_distance(123, "abc") == -1

    def test_not_string_second(self):
        assert hamming_distance("abc", 123) == -1

    def test_different_length(self):
        with pytest.raises(ValueError):
            hamming_distance("abc", "abcd")

    def test_both_empty(self):
        assert hamming_distance("", "") == 0

    def test_same_string(self):
        assert hamming_distance("father", "father") == 0

    def test_pip_pop(self):
        assert hamming_distance("pip", "pop") == 1

    def test_abcd_abab(self):
        assert hamming_distance("abcd", "abab") == 2

    def test_hello_hallo(self):
        assert hamming_distance("hello", "hallo") == 1

    def test_abcd_efgi(self):
        assert hamming_distance("abcd", "efgi") == 4

    def test_case_sensitive(self):
        assert hamming_distance("Hello", "hello") == 1

    def test_numbers_as_strings(self):
        assert hamming_distance("123", "124") == 1

    def test_long_strings(self):
        assert hamming_distance("abcdefgh", "abcdefgh") == 0
        assert hamming_distance("abcdefgh", "abcdefgi") == 1

    def test_empty_vs_non_empty(self):
        with pytest.raises(ValueError):
            hamming_distance("", "a")

    def test_unicode_characters(self):
        assert hamming_distance("Привет", "Привет") == 0
        assert hamming_distance("Привет", "Привeт") == 1
