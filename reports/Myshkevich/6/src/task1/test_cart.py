"""Тесты для мини-библиотеки покупок."""
from unittest.mock import patch, Mock

import pytest
from shopping import Cart, log_purchase, apply_coupon


# 1. ФИКСТУРА: пустая корзина
@pytest.fixture
def cart_fixture():
    """Фикстура, возвращающая пустую корзину."""
    return Cart()


# 2. ТЕСТЫ ДЛЯ ADD_ITEM И TOTAL
def test_add_item(cart_fixture):  # pylint: disable=W0621
    """Проверка добавления товара."""
    cart_fixture.add_item("Apple", 10.0)
    assert len(cart_fixture.items) == 1
    assert cart_fixture.items[0]["name"] == "Apple"
    assert cart_fixture.items[0]["price"] == 10.0


def test_add_item_negative_price(cart_fixture):  # pylint: disable=W0621
    """Проверка выброса ошибки при отрицательной цене."""
    with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
        cart_fixture.add_item("Orange", -5.0)


def test_total_empty_cart(cart_fixture):  # pylint: disable=W0621
    """Проверка общей стоимости пустой корзины."""
    assert cart_fixture.total() == 0.0


def test_total_with_items(cart_fixture):  # pylint: disable=W0621
    """Проверка общей стоимости с товарами."""
    cart_fixture.add_item("Apple", 10.0)
    cart_fixture.add_item("Banana", 20.0)
    assert cart_fixture.total() == 30.0


# 3. ТЕСТЫ ДЛЯ APPLY_DISCOUNT С @pytest.mark.parametrize
@pytest.mark.parametrize("discount, expected_total", [
    (0, 100.0),
    (50, 50.0),
    (100, 0.0),
])
def test_apply_discount_valid(cart_fixture, discount, expected_total):  # pylint: disable=W0621
    """Проверка применения корректных скидок."""
    cart_fixture.add_item("Laptop", 100.0)
    cart_fixture.apply_discount(discount)
    assert cart_fixture.total() == expected_total
    assert cart_fixture.discount == discount


@pytest.mark.parametrize("discount", [-10, -50, 110, 150, 200])
def test_apply_discount_invalid(cart_fixture, discount):  # pylint: disable=W0621
    """Проверка выброса ошибки при некорректных скидках."""
    cart_fixture.add_item("Phone", 500.0)
    with pytest.raises(ValueError, match="Скидка должна быть от 0 до 100 процентов"):
        cart_fixture.apply_discount(discount)


# 4. ТЕСТЫ ДЛЯ LOG_PURCHASE С МОКАНИЕМ HTTP-ЗАПРОСА
def test_log_purchase_mock():
    """Проверка логирования покупки с замоканным HTTP-запросом."""
    item = {"name": "Book", "price": 25.0}

    with patch("shopping.requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        log_purchase(item)

        mock_post.assert_called_once()
        mock_post.assert_called_with(
            "https://example.com/log",
            json=item,
            timeout=5
        )


def test_log_purchase_called_correctly():
    """Проверка, что log_purchase вызывается с корректными данными."""
    item = {"name": "Mouse", "price": 15.0}

    with patch("shopping.requests.post") as mock_post:
        log_purchase(item)

        args, kwargs = mock_post.call_args
        assert args[0] == "https://example.com/log"
        assert kwargs["json"] == item
        assert kwargs["timeout"] == 5


# 5. ТЕСТЫ ДЛЯ APPLY_COUPON
def test_apply_coupon_save10(cart_fixture):  # pylint: disable=W0621
    """Проверка купона SAVE10 (скидка 10%)."""
    cart_fixture.add_item("TV", 1000.0)
    apply_coupon(cart_fixture, "SAVE10")
    assert cart_fixture.total() == 900.0
    assert cart_fixture.discount == 10


def test_apply_coupon_half(cart_fixture):  # pylint: disable=W0621
    """Проверка купона HALF (скидка 50%)."""
    cart_fixture.add_item("Tablet", 200.0)
    apply_coupon(cart_fixture, "HALF")
    assert cart_fixture.total() == 100.0
    assert cart_fixture.discount == 50


def test_apply_coupon_invalid(cart_fixture):  # pylint: disable=W0621
    """Проверка выброса ошибки при неверном купоне."""
    cart_fixture.add_item("Book", 50.0)
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(cart_fixture, "INVALID")


def test_apply_coupon_discount_already_set(cart_fixture):  # pylint: disable=W0621
    """Проверка применения купона к корзине с существующей скидкой."""
    cart_fixture.add_item("Laptop", 1000.0)
    cart_fixture.apply_discount(20)
    apply_coupon(cart_fixture, "HALF")
    assert cart_fixture.discount == 50
    assert cart_fixture.total() == 500.0


# 6. ТЕСТ С MONKEYPATCH
def test_coupon_with_monkeypatch():
    """Проверка купонов с monkeypatch."""
    cart = Cart()
    cart.add_item("Test Item", 100.0)

    def patched_apply_coupon(cart_obj, coupon_code):
        coupons = {"TEST": 10}
        if coupon_code in coupons:
            cart_obj.apply_discount(coupons[coupon_code])
        else:
            raise ValueError("Invalid coupon")

    with patch("shopping.apply_coupon", patched_apply_coupon):
        patched_apply_coupon(cart, "TEST")
        assert cart.discount == 10
        assert cart.total() == 90.0
