"""Рефакторинг задач ЛР1 в функции для тестирования (ЛР6, задание 2)."""

from __future__ import annotations

from collections import Counter


def calculate_modes(numbers: list[int]) -> list[int]:
    """Возвращает отсортированный список мод; пустой список если моды нет."""
    if not numbers:
        return []
    counts = Counter(numbers)
    max_count = max(counts.values())
    modes = sorted(value for value, cnt in counts.items() if cnt == max_count)
    if max_count == 1 and len(modes) == len(numbers):
        return []
    return modes


def str_str(haystack: str, needle: str) -> int:
    """Аналог str.find: индекс первого вхождения needle, иначе -1."""
    if not needle:
        return 0
    if len(needle) > len(haystack):
        return -1
    for idx in range(len(haystack) - len(needle) + 1):
        if haystack[idx : idx + len(needle)] == needle:
            return idx
    return -1
