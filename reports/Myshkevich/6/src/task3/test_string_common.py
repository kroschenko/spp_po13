"""Тесты для метода common."""
import pytest
from string_common import common


def test_common_both_none():
    """Проверка: common(None, None) = TypeError."""
    with pytest.raises(TypeError):
        common(None, None)


def test_common_first_none():
    """Проверка: common(None, "abc") = TypeError."""
    with pytest.raises(TypeError):
        common(None, "abc")


def test_common_second_none():
    """Проверка: common("abc", None) = TypeError."""
    with pytest.raises(TypeError):
        common("abc", None)


def test_common_both_empty():
    """Проверка: common("", "") = ""."""
    assert common("", "") == ""


def test_common_first_empty_second_not():
    """Проверка: common("", " abc ") = ""."""
    assert common("", " abc ") == ""


def test_common_second_empty_first_not():
    """Проверка: common(" abc ", "") = ""."""
    assert common(" abc ", "") == ""


def test_common_with_spaces():
    """Проверка: common(" abc ", "abc") = "abc" (подстрока без пробелов)."""
    assert common(" abc ", "abc") == "abc"


def test_common_ab():
    """Проверка: common("ab", " abxyz ") = "ab"."""
    assert common("ab", " abxyz ") == "ab"


def test_common_abcde_abxyz():
    """Проверка: common(" abcde ", " abxyz ") = " ab " (с пробелами)."""
    assert common(" abcde ", " abxyz ") == " ab "


def test_common_no_match():
    """Проверка: common(" abcde ", " xyz ") = пробелы."""
    result = common(" abcde ", " xyz ")
    assert result in (" ", "  ", "")


def test_common_deabc():
    """Проверка: common(" deabc ", " abcdeabcd ") = " deabc " (с пробелами)."""
    result = common(" deabc ", " abcdeabcd ")
    assert result in ["deabc", "abc", " deabc "]


def test_common_fabce():
    """Проверка: common(" dfabcegt ", " rtoefabceiq ") = " fabce " (с пробелами)."""
    result = common(" dfabcegt ", " rtoefabceiq ")
    assert result in ["fabce", " fabce "]


# ==================== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ====================
def test_common_identical_strings():
    """Проверка: одинаковые строки."""
    assert common("hello", "hello") == "hello"


def test_common_one_string_contains_another():
    """Проверка: одна строка полностью содержится в другой."""
    assert common("abc", "xyzabcdef") == "abc"


def test_common_overlap_at_beginning():
    """Проверка: общая часть в начале."""
    assert common("abcdef", "abcxyz") == "abc"


def test_common_overlap_at_end():
    """Проверка: общая часть в конце."""
    assert common("xyzabc", "defabc") == "abc"


def test_common_overlap_in_middle():
    """Проверка: общая часть в середине."""
    assert common("ab123cd", "xy123zw") == "123"


def test_common_single_character():
    """Проверка: общая часть - один символ."""
    result = common("abc", "cba")
    assert result in ["a", "b", "c"]


def test_common_no_overlap():
    """Проверка: нет общей части."""
    assert common("abc", "def") == ""


def test_common_long_strings():
    """Проверка: длинные строки."""
    str1 = "x" * 100 + "common" + "y" * 100
    str2 = "z" * 50 + "common" + "w" * 50
    assert common(str1, str2) == "common"


def test_common_with_unicode():
    """Проверка: с русскими символами."""
    result = common("привет мир", "мир привет")
    assert result in ["привет", "мир"]


def test_common_case_sensitive():
    """Проверка: регистрозависимость."""
    assert common("ABC", "abc") == ""
