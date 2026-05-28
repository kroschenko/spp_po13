"""Tests for shopping cart module."""

from unittest.mock import patch

import pytest
from .shopping import Cart, log_purchase, apply_coupon


@pytest.fixture
def empty_cart():
    """Return empty cart instance."""
    return Cart()


def test_add_item(cart):
    """Test adding item to cart."""
    cart.add_item("Apple", 10.0)
    assert len(cart.items) == 1
    assert cart.items[0]["name"] == "Apple"
    assert cart.items[0]["price"] == 10.0


def test_negative_price(cart):
    """Test exception for negative price."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        cart.add_item("Banana", -5.0)


def test_total(cart):
    """Test total price calculation."""
    cart.add_item("Apple", 10.0)
    cart.add_item("Banana", 20.0)
    assert cart.total() == 30.0


@pytest.mark.parametrize("discount, expected", [
    (0, 100.0),
    (50, 50.0),
    (100, 0.0),
])
def test_apply_discount_valid(cart, discount, expected):
    """Test valid discount applications."""
    cart.add_item("Item", 100.0)
    cart.apply_discount(discount)
    assert cart.total() == expected


@pytest.mark.parametrize("discount", [-10, 110])
def test_apply_discount_invalid(cart, discount):
    """Test invalid discount values."""
    cart.add_item("Item", 100.0)
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        cart.apply_discount(discount)


def test_log_purchase():
    """Test log purchase with mock."""
    item = {"name": "Apple", "price": 10.0}
    with patch("shopping.requests.post") as mock_post:
        log_purchase(item)
        mock_post.assert_called_once_with(
            "https://example.com/log",
            json=item,
            timeout=5
        )


def test_apply_coupon_valid(cart, monkeypatch):
    """Test valid coupon application."""
    cart.add_item("Item", 100.0)
    monkeypatch.setitem(__import__("shopping").coupons, "TEST10", 10)
    apply_coupon(cart, "TEST10")
    assert cart.total() == 90.0


def test_apply_coupon_invalid(cart, monkeypatch):
    """Test invalid coupon application."""
    cart.add_item("Item", 100.0)
    monkeypatch.setitem(__import__("shopping").coupons, "TEST10", 10)
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart, "BADCODE")
