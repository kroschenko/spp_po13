import pytest
from lab1_functions import unique_numbers, add_binary

# Тесты для unique_numbers
def test_unique_numbers_trivial():
    assert unique_numbers([]) == []
    assert unique_numbers([1]) == [1]
    assert unique_numbers([1, 2, 3]) == [1, 2, 3]

def test_unique_numbers_with_duplicates():
    assert unique_numbers([1, 2, 2, 3, 3, 3]) == [1, 2, 3]
    assert unique_numbers([5, 5, 5]) == [5]

def test_unique_numbers_type_error():
    with pytest.raises(TypeError):
        unique_numbers("not a list")

# Тесты для add_binary
def test_add_binary_example():
    assert add_binary("11", "1") == "100"

def test_add_binary_zero():
    assert add_binary("0", "0") == "0"

def test_add_binary_carry():
    assert add_binary("111", "1") == "1000"
    assert add_binary("1010", "1011") == "10101"

def test_add_binary_with_leading_zeros():
    assert add_binary("001", "01") == "10"

def test_add_binary_type_error():
    with pytest.raises(TypeError):
        add_binary(123, "1")
