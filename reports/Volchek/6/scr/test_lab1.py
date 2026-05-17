"""Тесты к функциям из ЛР1 (ЛР6, задание 2)."""

from __future__ import annotations

import pytest

from lab1_refactored import calculate_modes, str_str


def test_calculate_modes_single_mode() -> None:
    assert calculate_modes([1, 2, 2, 3]) == [2]


def test_calculate_modes_multiple_modes() -> None:
    assert calculate_modes([1, 1, 2, 2, 3]) == [1, 2]


def test_calculate_modes_no_mode() -> None:
    assert calculate_modes([1, 2, 3, 4]) == []


def test_calculate_modes_empty_list() -> None:
    assert calculate_modes([]) == []


@pytest.mark.parametrize(
    ("haystack", "needle", "expected"),
    [
        ("hello", "ll", 2),
        ("aaaaa", "bba", -1),
        ("", "", 0),
        ("abc", "", 0),
        ("abc", "abc", 0),
        ("abc", "abcd", -1),
    ],
)
def test_str_str_cases(haystack: str, needle: str, expected: int) -> None:
    assert str_str(haystack, needle) == expected
