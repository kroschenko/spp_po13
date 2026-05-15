# test_repeat.py
import pytest

# ============================================
# Реализация метода repeat
# ============================================


def repeat(pattern, repeat_count):
    """
    Строит строку из указанного паттерна, повторённого заданное количество раз.

    Args:
        pattern (str): Строка-паттерн для повторения
        repeat_count (int): Количество повторений

    Returns:
        str: Строка, состоящая из повторённого паттерна

    Raises:
        TypeError: Если pattern не является строкой или repeat_count не является целым числом
        ValueError: Если repeat_count отрицательный
    """
    if not isinstance(pattern, str):
        raise TypeError(
            f"pattern должен быть строкой, получен {type(pattern).__name__}"
        )

    if not isinstance(repeat_count, int):
        raise TypeError(
            f"repeat_count должен быть целым числом, получен {type(repeat_count).__name__}"
        )

    if repeat_count < 0:
        raise ValueError("repeat_count не может быть отрицательным")

    if repeat_count == 0:
        return ""

    return pattern * repeat_count


# ============================================
# Фикстуры (должны быть объявлены до использования)
# ============================================


@pytest.fixture(name="simple_pattern")
def fixture_simple_pattern():
    """Простой паттерн для тестов"""
    return "abc"


@pytest.fixture(name="complex_pattern")
def fixture_complex_pattern():
    """Сложный паттерн для тестов"""
    return "Hello World! "


# ============================================
# Тесты для метода repeat
# ============================================


class TestRepeat:
    """Тесты для метода repeat"""

    # pylint: disable=too-many-public-methods

    # === Тесты по спецификации (с исправлением) ===

    def test_repeat_zero_times(self):
        """repeat("e", 0) = "" """
        assert repeat("e", 0) == ""

    def test_repeat_three_times(self):
        """repeat("e", 3) = "eee" """
        assert repeat("e", 3) == "eee"

    def test_repeat_with_spaces(self):
        """
        repeat(" ABC ", 2)
        Правильный результат: " ABC  ABC " (два пробела в середине)
        Примечание: спецификация содержит ошибку, показывая " ABCABC "
        """
        expected = " ABC  ABC "
        result = repeat(" ABC ", 2)
        assert result == expected
        assert len(result) == 10

    def test_repeat_with_spaces_detailed(self):
        """Детальная проверка repeat с пробелами"""
        pattern = " ABC "
        result = repeat(pattern, 2)

        assert result == pattern + pattern
        assert result == " ABC  ABC "
        assert result.startswith(" ")
        assert result.endswith(" ")
        assert "  " in result

    def test_repeat_negative_count(self):
        """repeat("e", -2) вызывает ValueError"""
        with pytest.raises(
            ValueError, match="repeat_count не может быть отрицательным"
        ):
            repeat("e", -2)

    def test_repeat_none_pattern(self):
        """repeat(None, 1) вызывает TypeError"""
        with pytest.raises(TypeError, match="pattern должен быть строкой"):
            repeat(None, 1)

    # === Тривиальные случаи ===

    def test_repeat_single_char_once(self):
        """Один символ один раз"""
        assert repeat("a", 1) == "a"

    def test_repeat_single_char_multiple_times(self):
        """Один символ много раз"""
        assert repeat("x", 5) == "xxxxx"

    def test_repeat_word_multiple_times(self):
        """Слово несколько раз"""
        assert repeat("Hello", 3) == "HelloHelloHello"

    def test_repeat_empty_string(self):
        """Пустая строка-паттерн"""
        assert repeat("", 5) == ""

    def test_repeat_empty_string_zero_times(self):
        """Пустая строка 0 раз"""
        assert repeat("", 0) == ""

    def test_repeat_special_characters(self):
        """Специальные символы"""
        assert repeat("!@#", 2) == "!@#!@#"

    def test_repeat_numbers_as_string(self):
        """Числа как строка"""
        assert repeat("123", 3) == "123123123"

    # === Граничные случаи ===

    def test_repeat_large_count(self):
        """Очень большое количество повторений"""
        result = repeat("a", 1000)
        assert len(result) == 1000
        assert result == "a" * 1000

    def test_repeat_one_million_times(self):
        """Миллион повторений (проверка производительности)"""
        result = repeat("a", 1000000)
        assert len(result) == 1000000

    def test_repeat_zero_with_empty_string(self):
        """Пустой паттерн 0 раз"""
        assert repeat("", 0) == ""

    def test_repeat_zero_with_long_pattern(self):
        """Длинный паттерн 0 раз"""
        assert repeat("very long pattern string", 0) == ""

    def test_repeat_unicode_characters(self):
        """Unicode символы"""
        assert repeat("😀", 3) == "😀😀😀"
        assert repeat("Привет", 2) == "ПриветПривет"

    def test_repeat_newline_characters(self):
        """Символы новой строки"""
        assert repeat("\n", 3) == "\n\n\n"

    def test_repeat_tab_characters(self):
        """Символы табуляции"""
        assert repeat("\t", 2) == "\t\t"

    def test_repeat_escape_sequences(self):
        """Escape-последовательности"""
        result = repeat("\\n", 2)
        assert result == "\\n\\n"

    # === Проверка спецификации с разными паттернами ===

    def test_repeat_no_spaces(self):
        """Паттерн без пробелов"""
        assert repeat("ABC", 2) == "ABCABC"
        assert repeat("ABC", 3) == "ABCABCABC"

    def test_repeat_leading_space(self):
        """Паттерн с пробелом в начале"""
        assert repeat(" ABC", 2) == " ABC ABC"

    def test_repeat_trailing_space(self):
        """Паттерн с пробелом в конце"""
        assert repeat("ABC ", 2) == "ABC ABC "

    def test_repeat_both_spaces(self):
        """Паттерн с пробелами с обеих сторон"""
        pattern = " ABC "
        assert repeat(pattern, 2) == pattern * 2

    # === Исключительные ситуации: TypeError ===

    def test_repeat_integer_pattern(self):
        """Целое число вместо строки"""
        with pytest.raises(TypeError, match="pattern должен быть строкой"):
            repeat(123, 1)

    def test_repeat_float_pattern(self):
        """Float вместо строки"""
        with pytest.raises(TypeError, match="pattern должен быть строкой"):
            repeat(3.14, 1)

    def test_repeat_list_pattern(self):
        """Список вместо строки"""
        with pytest.raises(TypeError, match="pattern должен быть строкой"):
            repeat([1, 2, 3], 1)

    def test_repeat_dict_pattern(self):
        """Словарь вместо строки"""
        with pytest.raises(TypeError, match="pattern должен быть строкой"):
            repeat({"key": "value"}, 1)

    def test_repeat_boolean_pattern(self):
        """Булево значение вместо строки"""
        with pytest.raises(TypeError, match="pattern должен быть строкой"):
            repeat(True, 1)

    def test_repeat_float_count(self):
        """Float вместо целого числа для repeat_count"""
        with pytest.raises(TypeError, match="repeat_count должен быть целым числом"):
            repeat("abc", 2.5)

    def test_repeat_string_count(self):
        """Строка вместо целого числа для repeat_count"""
        with pytest.raises(TypeError, match="repeat_count должен быть целым числом"):
            repeat("abc", "2")

    def test_repeat_none_count(self):
        """None вместо целого числа"""
        with pytest.raises(TypeError, match="repeat_count должен быть целым числом"):
            repeat("abc", None)

    def test_repeat_both_none(self):
        """Оба параметра None"""
        with pytest.raises(TypeError, match="pattern должен быть строкой"):
            repeat(None, None)

    # === Исключительные ситуации: ValueError ===

    def test_repeat_negative_one(self):
        """-1 повторений"""
        with pytest.raises(
            ValueError, match="repeat_count не может быть отрицательным"
        ):
            repeat("abc", -1)

    def test_repeat_negative_large(self):
        """Большое отрицательное число"""
        with pytest.raises(
            ValueError, match="repeat_count не может быть отрицательным"
        ):
            repeat("abc", -100)

    def test_repeat_negative_with_empty_string(self):
        """Отрицательное число с пустой строкой"""
        with pytest.raises(
            ValueError, match="repeat_count не может быть отрицательным"
        ):
            repeat("", -1)

    # === Дополнительные проверки ===

    def test_repeat_preserves_original_pattern(self):
        """Проверка, что оригинальный паттерн не изменяется"""
        pattern = "test"
        result = repeat(pattern, 3)
        assert pattern == "test"
        assert result == "testtesttest"

    def test_repeat_identity_with_one(self):
        """Повторение 1 раз возвращает ту же строку"""
        pattern = "hello world"
        result = repeat(pattern, 1)
        assert result == pattern

    def test_repeat_mutable_pattern_copy(self):
        """Проверка, что паттерн копируется, а не ссылается"""
        pattern = "abc"
        result = repeat(pattern, 2)
        assert result == "abcabc"
        assert result is not pattern

    def test_repeat_with_whitespace_only(self):
        """Паттерн только из пробелов"""
        assert repeat("   ", 2) == "      "

    def test_repeat_mixed_whitespace(self):
        """Паттерн с разными пробельными символами"""
        assert repeat(" \t\n", 2) == " \t\n \t\n"


# ============================================
# Параметризованные тесты
# ============================================


class TestRepeatParametrized:
    """Параметризованные тесты для repeat"""

    @pytest.mark.parametrize(
        "pattern,count,expected",
        [
            ("e", 0, ""),
            ("e", 3, "eee"),
            (" ABC ", 2, " ABC  ABC "),
            ("a", 1, "a"),
            ("", 5, ""),
            ("x", 10, "xxxxxxxxxx"),
            ("Hello", 2, "HelloHello"),
            ("😀", 3, "😀😀😀"),
            ("123", 0, ""),
            ("\n", 2, "\n\n"),
            ("ABC", 2, "ABCABC"),
            (" ABC", 2, " ABC ABC"),
            ("ABC ", 2, "ABC ABC "),
        ],
    )
    def test_repeat_valid_cases(self, pattern, count, expected):
        """Параметризованный тест корректных случаев"""
        result = repeat(pattern, count)
        assert result == expected

    @pytest.mark.parametrize(
        "pattern,count,expected_error,error_msg",
        [
            ("e", -2, ValueError, "repeat_count не может быть отрицательным"),
            (None, 1, TypeError, "pattern должен быть строкой"),
            ("abc", -1, ValueError, "repeat_count не может быть отрицательным"),
            (123, 1, TypeError, "pattern должен быть строкой"),
            ("abc", 2.5, TypeError, "repeat_count должен быть целым числом"),
            ([1, 2], 1, TypeError, "pattern должен быть строкой"),
            ("test", "3", TypeError, "repeat_count должен быть целым числом"),
            (True, 5, TypeError, "pattern должен быть строкой"),
        ],
    )
    def test_repeat_invalid_cases(self, pattern, count, expected_error, error_msg):
        """Параметризованный тест некорректных случаев"""
        with pytest.raises(expected_error, match=error_msg):
            repeat(pattern, count)

    @pytest.mark.parametrize("count", [0, 1, 2, 5, 10, 100])
    def test_repeat_various_counts(self, count):
        """Тест с разным количеством повторений"""
        result = repeat("x", count)
        assert len(result) == count
        assert result == "x" * count


# ============================================
# Тесты с фикстурами
# ============================================


def test_repeat_with_simple_fixture(simple_pattern):
    """Тест с простой фикстурой"""
    result = repeat(simple_pattern, 3)
    assert result == "abcabcabc"
    assert len(result) == 9


def test_repeat_with_complex_fixture(complex_pattern):
    """Тест со сложной фикстурой"""
    result = repeat(complex_pattern, 2)
    assert result == "Hello World! Hello World! "


# ============================================
# Интеграционные тесты
# ============================================


def test_repeat_in_string_operations():
    """Использование repeat в строковых операциях"""
    pattern = "Ha"
    laughter = repeat(pattern, 3)
    assert laughter + "!" == "HaHaHa!"
    assert len(laughter) == 6


def test_repeat_with_concatenation():
    """Конкатенация с repeat"""
    part1 = repeat("AB", 2)
    part2 = repeat("CD", 3)
    assert part1 + part2 == "ABABCDCDCD"


def test_repeat_to_build_pyramid():
    """Построение пирамиды с помощью repeat"""
    lines = []
    for i in range(1, 4):
        spaces = repeat(" ", 3 - i)
        stars = repeat("*", 2 * i - 1)
        lines.append(spaces + stars)
    expected = ["  *", " ***", "*****"]
    assert lines == expected


# ============================================
# Запуск тестов
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
