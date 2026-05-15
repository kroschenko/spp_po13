"""Тесты для keep (ЛР6, задание 3, вариант 3)."""

from __future__ import annotations

import pytest

from string_variant3 import keep


def test_keep_none_none_raises_type_error() -> None:
    with pytest.raises(TypeError):
        keep(None, None)


def test_keep_none_star_returns_none() -> None:
    assert keep(None, "abc") is None


def test_keep_empty_source_returns_empty() -> None:
    assert keep("", "abc") == ""


def test_keep_star_none_returns_empty() -> None:
    assert keep("abc", None) == ""


def test_keep_star_empty_pattern_returns_empty() -> None:
    assert keep("abc", "") == ""


def test_keep_hello_hl() -> None:
    assert keep("hello", "hl") == "hll"


def test_keep_hello_le() -> None:
    assert keep("hello", "le") == "ell"
