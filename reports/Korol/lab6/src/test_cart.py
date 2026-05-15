from unittest.mock import patch

import pytest

from shopping import Cart


@pytest.fixture
def empty_cart():
    return Cart()


def test_add_item(empty_cart):
    empty_cart.add_item("Apple", 10)

    assert len(empty_cart.items) == 1


def test_negative_price(empty_cart):
    with pytest.raises(ValueError):
        empty_cart.add_item("Apple", -10)


def test_total(empty_cart):
    empty_cart.add_item("Apple", 10)
    empty_cart.add_item("Orange", 20)

    assert empty_cart.total() == 30


@pytest.mark.parametrize(
    "discount, result",
    [
        (0, 100),
        (50, 50),
        (100, 0),
    ],
)
def test_apply_discount(discount, result):
    cart = Cart()

    cart.add_item("Apple", 100)

    cart.apply_discount(discount)

    assert cart.items[0]["price"] == result


@pytest.mark.parametrize(
    "discount",
    [-1, 101],
)
def test_invalid_discount(discount):
    cart = Cart()

    cart.add_item("Apple", 100)

    with pytest.raises(ValueError):
        cart.apply_discount(discount)


def log_purchase(item):
    import requests

    requests.post(
        "https://example.com/log",
        json=item,
        timeout=10,
    )


@patch("requests.post")
def test_log_purchase(mock_post):
    item = {
        "name": "Apple",
        "price": 10,
    }

    log_purchase(item)

    mock_post.assert_called_once_with(
        "https://example.com/log",
        json=item,
        timeout=10,
    )
