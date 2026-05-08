import pytest
from shopping import Cart

@pytest.fixture(name='cart')
def empty_cart_fixture():
    """Returns a new empty cart."""
    return Cart()

def test_add_item(cart):
    cart.add_item("apple", 1.5, 2)
    assert len(cart) == 2
    assert cart.total() == 3.0

def test_add_duplicate_item(cart):
    cart.add_item("banana", 2.0, 1)
    cart.add_item("banana", 2.0, 3)
    assert len(cart) == 4
    assert cart.total() == 8.0

def test_add_invalid_price(cart):
    with pytest.raises(ValueError):
        cart.add_item("bad", -1.0, 1)

def test_remove_item(cart):
    cart.add_item("orange", 3.0, 5)
    cart.remove_item("orange", 2)
    assert len(cart) == 3
    assert cart.total() == 9.0

def test_remove_too_much(cart):
    cart.add_item("pear", 1.0, 1)
    with pytest.raises(ValueError):
        cart.remove_item("pear", 2)

def test_remove_missing_item(cart):
    with pytest.raises(KeyError):
        cart.remove_item("nonexistent")

def test_clear(cart):
    cart.add_item("a", 1, 2)
    cart.add_item("b", 2, 3)
    cart.clear()
    assert len(cart) == 0
    assert cart.total() == 0.0
