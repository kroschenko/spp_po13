"""Тесты задания 1 ЛР6 для shopping.py."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from shopping import COUPONS, Cart, apply_coupon, log_purchase


@pytest.fixture
def empty_cart() -> Cart:
    return Cart()


def test_add_item_adds_one_element(empty_cart: Cart) -> None:
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"


def test_add_item_raises_for_negative_price(empty_cart: Cart) -> None:
    with pytest.raises(ValueError):
        empty_cart.add_item("Bad", -1.0)


def test_total_calculates_sum(empty_cart: Cart) -> None:
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Milk", 5.5)
    assert empty_cart.total() == pytest.approx(15.5)


@pytest.mark.parametrize(
    ("discount", "expected"),
    [
        (0, 100.0),
        (50, 50.0),
        (100, 0.0),
    ],
)
def test_apply_discount_values(empty_cart: Cart, discount: float, expected: float) -> None:
    empty_cart.add_item("Item", 100.0)
    empty_cart.apply_discount(discount)
    assert empty_cart.total() == pytest.approx(expected)


@pytest.mark.parametrize("discount", [-1, 101])
def test_apply_discount_out_of_range_raises(empty_cart: Cart, discount: float) -> None:
    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)


@patch("shopping.requests.post")
def test_log_purchase_calls_requests_post(mock_post) -> None:
    payload = {"name": "Apple", "price": 10.0}
    log_purchase(payload)
    mock_post.assert_called_once_with("https://example.com/log", json=payload, timeout=10)


def test_apply_coupon_valid_default(empty_cart: Cart) -> None:
    empty_cart.add_item("Apple", 100.0)
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == pytest.approx(90.0)


def test_apply_coupon_invalid_raises(empty_cart: Cart) -> None:
    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "UNKNOWN")


def test_apply_coupon_with_patch_dict(empty_cart: Cart) -> None:
    empty_cart.add_item("Apple", 200.0)
    with patch.dict(COUPONS, {"SUPER": 25}, clear=True):
        apply_coupon(empty_cart, "SUPER")
    assert empty_cart.total() == pytest.approx(150.0)
