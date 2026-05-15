# pylint: disable=redefined-outer-name,import-error

"""Тесты для мини-библиотеки покупок."""

from unittest.mock import patch

import pytest

import shopping
from shopping import Cart, apply_coupon, log_purchase


@pytest.fixture
def empty_cart():
    """Создает пустую корзину."""
    return Cart()


def test_add_item(empty_cart):
    """Проверяет добавление товара."""
    empty_cart.add_item("Apple", 10.0)

    assert len(empty_cart.items) == 1


def test_add_item_negative_price(empty_cart):
    """Проверяет ошибку при отрицательной цене."""
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -10.0)


def test_total(empty_cart):
    """Проверяет вычисление общей стоимости."""
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Milk", 20.0)

    assert empty_cart.total() == 30.0


@pytest.mark.parametrize(
    ("discount", "expected"),
    [
        (0, 100.0),
        (50, 50.0),
        (100, 0.0),
    ],
)
def test_apply_discount(empty_cart, discount, expected):
    """Проверяет применение скидки."""
    empty_cart.add_item("Apple", 100.0)

    empty_cart.apply_discount(discount)

    assert empty_cart.total() == expected


@pytest.mark.parametrize("discount", [-1, 101])
def test_apply_discount_invalid(empty_cart, discount):
    """Проверяет ошибку при неверной скидке."""
    empty_cart.add_item("Apple", 100.0)

    with pytest.raises(ValueError):
        empty_cart.apply_discount(discount)


@patch("shopping.requests.post")
def test_log_purchase(mock_post):
    """Проверяет логирование покупки без реального HTTP-запроса."""
    item = {"name": "Apple", "price": 10.0}

    log_purchase(item)

    mock_post.assert_called_once_with("https://example.com/log", json=item)


def test_apply_coupon_save10(empty_cart):
    """Проверяет купон SAVE10."""
    empty_cart.add_item("Apple", 100.0)

    apply_coupon(empty_cart, "SAVE10")

    assert empty_cart.total() == 90.0


def test_apply_coupon_half(empty_cart):
    """Проверяет купон HALF."""
    empty_cart.add_item("Apple", 100.0)

    apply_coupon(empty_cart, "HALF")

    assert empty_cart.total() == 50.0


def test_apply_coupon_invalid(empty_cart):
    """Проверяет ошибку при неверном купоне."""
    empty_cart.add_item("Apple", 100.0)

    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "BAD")


def test_apply_coupon_monkeypatch(empty_cart, monkeypatch):
    """Проверяет подмену словаря купонов."""
    monkeypatch.setattr(shopping, "COUPONS", {"TEST": 25})
    empty_cart.add_item("Apple", 100.0)

    apply_coupon(empty_cart, "TEST")

    assert empty_cart.total() == 75.0
