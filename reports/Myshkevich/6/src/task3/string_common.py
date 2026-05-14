"""Модуль с методом common для поиска наибольшей общей части."""
from typing import Optional


def common(str1: Optional[str], str2: Optional[str]) -> str:
    """
    Находит наибольшую общую часть двух строк.
    (Общая часть может быть НЕ непрерывной подстрокой!)

    Args:
        str1: Первая строка
        str2: Вторая строка

    Returns:
        Наибольшая общая часть

    Raises:
        TypeError: Если один из аргументов None
    """
    # Проверка на None
    if str1 is None or str2 is None:
        raise TypeError("Arguments cannot be None")

    # Проверка на пустые строки
    if not str1 or not str2:
        return ""

    len1, len2 = len(str1), len(str2)

    # Создаем матрицу для LCS (Longest Common Subsequence)
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    # Заполняем матрицу
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Восстанавливаем строку
    result_chars = []
    i, j = len1, len2
    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            result_chars.append(str1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    # Переворачиваем, так как собирали с конца
    return ''.join(reversed(result_chars))
