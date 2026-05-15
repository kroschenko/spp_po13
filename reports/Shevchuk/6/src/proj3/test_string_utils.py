# pylint: disable=import-error

"""Тесты для substringBetween, вариант 7."""

import pytest

from string_utils import substringBetween


def test_substring_between_none_none_none():
    """Проверяет TypeError для трех None."""
    with pytest.raises(TypeError):
        substringBetween(None, None, None)


@pytest.mark.parametrize(
    ("text", "open_token", "close_token", "expected"),
    [
        (None, "[", "]", None),
        ("abc", None, "]", None),
        ("abc", "[", None, None),
        ("", "", "", ""),
        ("", "", "]", None),
        ("", "[", "]", None),
        ("yabcz", "", "", ""),
        ("yabcz", "y", "z", "abc"),
        ("yabczyabcz", "y", "z", "abc"),
        ("wx[b]yz", "[", "]", "b"),
    ],
)
def test_substring_between(text, open_token, close_token, expected):
    """Проверяет функцию по спецификации."""
    assert substringBetween(text, open_token, close_token) == expected
