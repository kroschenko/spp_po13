from unittest.mock import patch

import pytest
import requests

from shopping import Cart


@pytest.fixture
def cart_fixture():
    return Cart()


def test_add_item(cart_fixture):
    cart_fixture.add_item("Apple", 10)

    assert len(cart_fixture.items) == 1


def test_negative_price(cart_fixture):
    with pytest.raises(ValueError):
        cart_fixture.add_item("Apple", -10)


def test_total(cart_fixture):
    cart_fixture.add_item("Apple", 10)

    cart_fixture.add_item("Orange", 20)

    assert cart_fixture.total() == 30


@pytest.mark.parametrize(
    ("discount", "result"),
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
