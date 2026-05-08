import pytest
from shopping import Cart

@pytest.fixture
def empty_cart():
    """Returns a new empty cart."""
    return Cart()

def test_add_item(empty_cart):
    empty_cart.add_item("apple", 1.5, 2)
    assert len(empty_cart) == 2
    assert empty_cart.total() == 3.0

def test_add_duplicate_item(empty_cart):
    empty_cart.add_item("banana", 2.0, 1)
    empty_cart.add_item("banana", 2.0, 3)
    assert len(empty_cart) == 4
    assert empty_cart.total() == 8.0

def test_add_invalid_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("bad", -1.0, 1)

def test_remove_item(empty_cart):
    empty_cart.add_item("orange", 3.0, 5)
    empty_cart.remove_item("orange", 2)
    assert len(empty_cart) == 3
    assert empty_cart.total() == 9.0

def test_remove_too_much(empty_cart):
    empty_cart.add_item("pear", 1.0, 1)
    with pytest.raises(ValueError):
        empty_cart.remove_item("pear", 2)

def test_remove_missing_item(empty_cart):
    with pytest.raises(KeyError):
        empty_cart.remove_item("nonexistent")

def test_clear(empty_cart):
    empty_cart.add_item("a", 1, 2)
    empty_cart.add_item("b", 2, 3)
    empty_cart.clear()
    assert len(empty_cart) == 0
    assert empty_cart.total() == 0.0
