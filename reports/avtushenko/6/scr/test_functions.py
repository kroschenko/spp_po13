# test_functions.py
import pytest

# ============================================
# Функции для тестирования
# ============================================


def check_equal(sequence):
    """
    Проверяет, все ли элементы последовательности равны.
    Возвращает "равны", если все равны, иначе "не равны".
    """
    if not sequence:  # пустая последовательность
        return "не равны"

    # Сравниваем каждый элемент с первым
    first = sequence[0]
    for item in sequence:
        if item != first:
            return "не равны"
    return "равны"


def two_sum(nums, target):
    """
    Находит индексы двух чисел, сумма которых равна target.
    Возвращает список из двух индексов или None.
    """
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None


# ============================================
# Фикстуры (должны быть объявлены до использования)
# ============================================


@pytest.fixture
def sample_numbers():
    """Пример числовой последовательности"""
    return [1, 2, 3, 4, 5]


@pytest.fixture
def sample_equal_numbers():
    """Последовательность равных чисел"""
    return [7, 7, 7, 7]


@pytest.fixture
def two_sum_test_data():
    """Тестовые данные для two_sum"""
    return {"nums": [2, 7, 11, 15], "target": 9, "expected": [0, 1]}


# ============================================
# Тесты для check_equal
# ============================================


class TestCheckEqual:
    """Тесты для функции check_equal"""

    # === Тривиальные случаи ===

    @staticmethod
    def test_all_equal_numbers():
        """Все числа равны"""
        assert check_equal([5, 5, 5, 5]) == "равны"

    @staticmethod
    def test_not_equal_numbers():
        """Числа не равны"""
        assert check_equal([1, 2, 3, 4]) == "не равны"

    @staticmethod
    def test_all_equal_strings():
        """Все строки равны"""
        assert check_equal(["a", "a", "a"]) == "равны"

    @staticmethod
    def test_not_equal_strings():
        """Строки не равны"""
        assert check_equal(["a", "b", "c"]) == "не равны"

    @staticmethod
    def test_all_equal_floats():
        """Все float числа равны"""
        assert check_equal([3.14, 3.14, 3.14]) == "равны"

    @staticmethod
    def test_not_equal_floats():
        """Float числа не равны"""
        assert check_equal([3.14, 2.71, 1.41]) == "не равны"

    # === Граничные случаи ===

    @staticmethod
    def test_single_element():
        """Последовательность из одного элемента"""
        assert check_equal([42]) == "равны"

    @staticmethod
    def test_single_element_none():
        """Единственный элемент None"""
        assert check_equal([None]) == "равны"

    @staticmethod
    def test_two_equal_elements():
        """Два равных элемента"""
        assert check_equal([7, 7]) == "равны"

    @staticmethod
    def test_two_not_equal_elements():
        """Два разных элемента"""
        assert check_equal([7, 8]) == "не равны"

    @staticmethod
    def test_first_different():
        """Первый элемент отличается"""
        assert check_equal([1, 2, 2, 2]) == "не равны"

    @staticmethod
    def test_last_different():
        """Последний элемент отличается"""
        assert check_equal([2, 2, 2, 1]) == "не равны"

    @staticmethod
    def test_middle_different():
        """Средний элемент отличается"""
        assert check_equal([2, 2, 1, 2, 2]) == "не равны"

    @staticmethod
    def test_large_sequence_equal():
        """Большая последовательность равных элементов"""
        assert check_equal([1] * 1000) == "равны"

    @staticmethod
    def test_large_sequence_not_equal():
        """Большая последовательность с разными элементами"""
        seq = [1] * 999 + [2]
        assert check_equal(seq) == "не равны"

    # === Пустая последовательность ===

    @staticmethod
    def test_empty_list():
        """Пустой список"""
        assert check_equal([]) == "не равны"

    @staticmethod
    def test_empty_tuple():
        """Пустой кортеж"""
        assert check_equal(()) == "не равны"

    @staticmethod
    def test_empty_string():
        """Пустая строка"""
        assert check_equal("") == "не равны"

    # === Специальные типы данных ===

    @staticmethod
    def test_boolean_values_equal():
        """Булевы значения (равны)"""
        assert check_equal([True, True, True]) == "равны"

    @staticmethod
    def test_boolean_values_not_equal():
        """Булевы значения (не равны)"""
        assert check_equal([True, False, True]) == "не равны"

    @staticmethod
    def test_mixed_types():
        """Смешанные типы данных"""
        assert check_equal([1, "1", 1.0]) == "не равны"

    @staticmethod
    def test_none_values_equal():
        """Все None значения"""
        assert check_equal([None, None, None]) == "равны"

    @staticmethod
    def test_none_and_value():
        """None и другие значения"""
        assert check_equal([None, 1]) == "не равны"

    # === Нестандартные последовательности ===

    @staticmethod
    def test_tuple_input():
        """Кортеж на входе"""
        assert check_equal((5, 5, 5)) == "равны"

    @staticmethod
    def test_string_input_equal():
        """Строка с одинаковыми символами"""
        assert check_equal("aaaa") == "равны"

    @staticmethod
    def test_string_input_not_equal():
        """Строка с разными символами"""
        assert check_equal("abcd") == "не равны"

    @staticmethod
    def test_range_object():
        """Объект range"""
        assert check_equal(range(1, 5)) == "не равны"

    @staticmethod
    def test_list_of_lists_equal():
        """Список одинаковых списков"""
        assert check_equal([[1, 2], [1, 2], [1, 2]]) == "равны"

    @staticmethod
    def test_list_of_lists_not_equal():
        """Список разных списков"""
        assert check_equal([[1, 2], [3, 4]]) == "не равны"

    # === Исключительные ситуации ===

    @staticmethod
    def test_none_input():
        """None как входной параметр (None считается falsy, возвращает "не равны")"""
        result = check_equal(None)
        assert result == "не равны"

    @staticmethod
    def test_integer_input():
        """Целое число вместо последовательности"""
        with pytest.raises(TypeError):
            check_equal(42)

    @staticmethod
    def test_generator_input():
        """Генератор (нельзя индексировать)"""
        gen = (x for x in [1, 1, 1])
        with pytest.raises(TypeError):
            check_equal(gen)

    @staticmethod
    def test_uncomparable_objects():
        """Объекты, которые нельзя сравнить"""

        class Uncomparable:
            def __eq__(self, other):
                raise ValueError("Cannot compare")

        with pytest.raises(ValueError):
            check_equal([Uncomparable(), Uncomparable()])


# ============================================
# Тесты для two_sum
# ============================================


class TestTwoSum:
    """Тесты для функции two_sum"""

    # === Тривиальные случаи ===

    @staticmethod
    def test_simple_case():
        """Простой случай"""
        assert two_sum([2, 7, 11, 15], 9) == [0, 1]

    @staticmethod
    def test_same_number_twice():
        """Одно и то же число дважды"""
        assert two_sum([3, 3], 6) == [0, 1]

    @staticmethod
    def test_negative_numbers():
        """Отрицательные числа"""
        assert two_sum([-3, 4, 3, 90], 0) == [0, 2]

    @staticmethod
    def test_zero_target():
        """Нулевая цель"""
        result = two_sum([1, -1, 2, -2], 0)
        assert result is not None
        assert len(result) == 2
        assert result[0] != result[1]

    @staticmethod
    def test_large_numbers():
        """Большие числа"""
        result = two_sum([1000000, 2000000, 3000000], 5000000)
        assert result == [1, 2]

    # === Граничные случаи ===

    @staticmethod
    def test_two_elements_found():
        """Ровно два элемента (решение есть)"""
        assert two_sum([1, 2], 3) == [0, 1]

    @staticmethod
    def test_two_elements_not_found():
        """Ровно два элемента (решения нет)"""
        assert two_sum([1, 2], 4) is None

    @staticmethod
    def test_solution_at_beginning():
        """Решение в начале массива"""
        assert two_sum([1, 2, 3, 4, 5], 3) == [0, 1]

    @staticmethod
    def test_solution_at_end():
        """Решение в конце массива"""
        assert two_sum([1, 2, 3, 4, 5], 9) == [3, 4]

    @staticmethod
    def test_solution_far_apart():
        """Элементы далеко друг от друга (проверяем правильность суммы, а не конкретные индексы)"""
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 11
        result = two_sum(nums, target)
        assert result is not None
        assert len(result) == 2
        assert result[0] != result[1]
        assert nums[result[0]] + nums[result[1]] == target

    @staticmethod
    def test_multiple_solutions_returns_first():
        """Несколько решений (возвращает первое найденное)"""
        result = two_sum([1, 2, 3, 1], 4)
        assert result is not None
        assert result[0] != result[1]
        nums = [1, 2, 3, 1]
        assert nums[result[0]] + nums[result[1]] == 4

    @staticmethod
    def test_different_indices_required():
        """Нельзя использовать один и тот же индекс дважды"""
        nums = [2, 1, 3]
        target = 4
        result = two_sum(nums, target)
        assert result is not None
        assert result[0] != result[1]
        assert nums[result[0]] + nums[result[1]] == target

    # === Пустые и маленькие последовательности ===

    @staticmethod
    def test_empty_list():
        """Пустой список"""
        assert two_sum([], 5) is None

    @staticmethod
    def test_single_element():
        """Один элемент"""
        assert two_sum([5], 5) is None

    @staticmethod
    def test_single_element_zero():
        """Один элемент равен цели"""
        assert two_sum([0], 0) is None

    # === Нули и специальные значения ===

    @staticmethod
    def test_all_zeros():
        """Все нули"""
        result = two_sum([0, 0, 0], 0)
        assert result == [0, 1]

    @staticmethod
    def test_target_zero_with_various_numbers():
        """Цель 0 с разными числами (проверяем правильность суммы)"""
        nums = [1, 0, -1, 2]
        target = 0
        result = two_sum(nums, target)
        assert result is not None
        assert result[0] != result[1]
        assert nums[result[0]] + nums[result[1]] == target

    @staticmethod
    def test_duplicate_numbers():
        """Дубликаты чисел"""
        result = two_sum([1, 2, 2, 3], 4)
        assert result is not None
        assert result[0] != result[1]
        nums = [1, 2, 2, 3]
        assert nums[result[0]] + nums[result[1]] == 4

    @staticmethod
    def test_very_large_array():
        """Очень большой массив"""
        nums = list(range(10000))
        target = 19997
        result = two_sum(nums, target)
        assert result is not None
        assert nums[result[0]] + nums[result[1]] == target

    # === Float числа ===

    @staticmethod
    def test_float_numbers():
        """Float числа"""
        result = two_sum([1.5, 2.5, 3.5], 4.0)
        assert result == [0, 1]

    @staticmethod
    def test_float_precision():
        """Точность float"""
        result = two_sum([0.1, 0.2, 0.3], 0.5)
        assert result is not None
        nums = [0.1, 0.2, 0.3]
        assert abs(nums[result[0]] + nums[result[1]] - 0.5) < 0.0001

    # === Исключительные ситуации ===

    @staticmethod
    def test_none_input_list():
        """None вместо списка"""
        with pytest.raises(TypeError):
            two_sum(None, 5)

    @staticmethod
    def test_none_target():
        """None вместо цели"""
        with pytest.raises(TypeError):
            two_sum([1, 2, 3], None)

    @staticmethod
    def test_string_in_list():
        """Строка в списке чисел"""
        with pytest.raises(TypeError):
            two_sum([1, "2", 3], 5)

    @staticmethod
    def test_target_not_number():
        """Цель не число"""
        with pytest.raises(TypeError):
            two_sum([1, 2, 3], "5")

    @staticmethod
    def test_list_with_none():
        """None в списке"""
        with pytest.raises(TypeError):
            two_sum([1, None, 3], 4)

    @staticmethod
    def test_non_list_input():
        """Не список на входе"""
        with pytest.raises(TypeError):
            two_sum("123", 5)

    @staticmethod
    def test_mixed_types_in_list():
        """Смешанные типы в списке"""
        with pytest.raises(TypeError):
            two_sum([1, 2.5, "3"], 5)

    # === Дополнительные проверки ===

    @staticmethod
    def test_result_indices_are_different():
        """Проверка, что индексы разные"""
        result = two_sum([1, 2, 3], 5)
        if result:
            assert result[0] != result[1]

    @staticmethod
    def test_result_is_correct():
        """Проверка правильности результата"""
        nums = [3, 7, 11, 15]
        target = 18
        result = two_sum(nums, target)
        assert result is not None
        assert nums[result[0]] + nums[result[1]] == target

    @staticmethod
    def test_order_of_indices():
        """Проверка порядка индексов (первый меньше второго)"""
        result = two_sum([5, 3, 8, 2], 10)
        if result:
            assert result[0] < result[1]


# ============================================
# Параметризованные тесты
# ============================================


class TestParametrized:
    """Параметризованные тесты"""

    @pytest.mark.parametrize(
        "sequence,expected",
        [
            ([1, 1, 1], "равны"),
            ([1, 2, 1], "не равны"),
            (["a", "a"], "равны"),
            (["a", "b"], "не равны"),
            ([True, True], "равны"),
            ([True, False], "не равны"),
            ([], "не равны"),
            ([42], "равны"),
        ],
    )
    @staticmethod
    def test_check_equal_parametrized(sequence, expected):
        """Параметризованный тест check_equal"""
        assert check_equal(sequence) == expected

    @pytest.mark.parametrize(
        "nums,target,expected",
        [
            ([2, 7, 11, 15], 9, [0, 1]),
            ([3, 2, 4], 6, [1, 2]),
            ([3, 3], 6, [0, 1]),
            ([1, 2, 3], 7, None),
            ([], 5, None),
            ([1], 1, None),
            ([-1, -2, -3, -4, -5], -8, [2, 4]),
        ],
    )
    @staticmethod
    def test_two_sum_parametrized(nums, target, expected):
        """Параметризованный тест two_sum"""
        assert two_sum(nums, target) == expected


# ============================================
# Тесты с фикстурами
# ============================================


def test_with_fixture_equal(sample_equal_numbers):
    """Тест с фикстурой равных чисел"""
    assert check_equal(sample_equal_numbers) == "равны"


def test_with_fixture_not_equal(sample_numbers):
    """Тест с фикстурой разных чисел"""
    assert check_equal(sample_numbers) == "не равны"


def test_two_sum_with_fixture(two_sum_test_data):
    """Тест two_sum с фикстурой"""
    result = two_sum(two_sum_test_data["nums"], two_sum_test_data["target"])
    assert result == two_sum_test_data["expected"]


# ============================================
# Интеграционные тесты (дополнительные)
# ============================================


def test_check_equal_with_two_sum_result():
    """Интеграционный тест: использование check_equal с результатом two_sum"""
    nums = [5, 5, 5, 5]
    result = two_sum(nums, 10)
    assert result is not None
    found_numbers = [nums[result[0]], nums[result[1]]]
    assert check_equal(found_numbers) == "равны"


def test_real_world_scenario():
    """Реалистичный сценарий использования"""
    prices = [100, 100, 100, 100]
    assert check_equal(prices) == "равны"

    result = two_sum(prices, 200)
    assert result is not None
    assert prices[result[0]] + prices[result[1]] == 200


# ============================================
# Запуск тестов
# ============================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
