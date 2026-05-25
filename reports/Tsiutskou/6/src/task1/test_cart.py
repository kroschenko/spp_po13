from unittest.mock import patch
import pytest
from shopping import Item, Cart, apply_coupon, log_purchase


@pytest.fixture
def empty_cart():
    return Cart()


class TestCart:
    def test_add_item(self, empty_cart):
        cart_instance = empty_cart
        cart_instance.add_item(Item("Apple", 10.0))
        assert len(cart_instance.items) == 1

    def test_negative_price(self):
        with pytest.raises(ValueError):
            Item("Bad", -5.0)

    def test_total(self, empty_cart):
        cart_instance = empty_cart
        cart_instance.add_item(Item("Apple", 10.0))
        cart_instance.add_item(Item("Banana", 20.0))
        assert cart_instance.total() == 30.0

    @pytest.mark.parametrize("discount,expected", [(0, 30.0), (50, 15.0), (100, 0.0)])
    def test_apply_discount(self, empty_cart, discount, expected):
        cart_instance = empty_cart
        cart_instance.add_item(Item("Apple", 10.0))
        cart_instance.add_item(Item("Banana", 20.0))
        cart_instance.apply_discount(discount)
        assert cart_instance.total() == expected

    @pytest.mark.parametrize("discount", [-10, 110])
    def test_invalid_discount(self, empty_cart, discount):
        cart_instance = empty_cart
        with pytest.raises(ValueError):
            cart_instance.apply_discount(discount)


class TestCoupon:
    def test_apply_save10(self, empty_cart):
        cart_instance = empty_cart
        cart_instance.add_item(Item("Apple", 100))
        apply_coupon(cart_instance, "SAVE10")
        assert cart_instance.discount_percent == 10

    def test_apply_half(self, empty_cart):
        cart_instance = empty_cart
        cart_instance.add_item(Item("Apple", 100))
        apply_coupon(cart_instance, "HALF")
        assert cart_instance.discount_percent == 50

    def test_invalid_coupon(self, empty_cart):
        cart_instance = empty_cart
        with pytest.raises(ValueError):
            apply_coupon(cart_instance, "INVALID")

    def test_mock_coupons_with_patch_dict(self, empty_cart):
        cart_instance = empty_cart
        cart_instance.add_item(Item("Apple", 100))
        with patch.dict("shopping.coupons", {"TEST": 20}, clear=True):
            apply_coupon(cart_instance, "TEST")
            assert cart_instance.discount_percent == 20


class TestLogPurchase:
    @patch("shopping.requests.post")
    def test_log_purchase_calls_post(self, mock_post):
        item = Item("Apple", 10.0)
        log_purchase(item)
        mock_post.assert_called_once_with("https://example.com/log", json={"name": "Apple", "price": 10.0}, timeout=5)
