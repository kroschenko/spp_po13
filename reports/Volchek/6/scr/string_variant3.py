"""ЛР6, задание 3, вариант 3: keep(str, pattern)."""

from __future__ import annotations


def keep(source: str | None, pattern: str | None) -> str | None:
    """
    Оставляет в source только символы, которые есть в pattern.

    Спецификация варианта:
    - keep(None, None) -> TypeError
    - keep(None, *) -> None
    - keep("", *) -> ""
    - keep(*, None) -> ""
    - keep(*, "") -> ""
    """
    if source is None and pattern is None:
        raise TypeError("source and pattern cannot be both None")
    if source is None:
        return None
    if source == "":
        return ""
    if pattern is None or pattern == "":
        return ""

    allowed = set(pattern)
    return "".join(ch for ch in source if ch in allowed)
