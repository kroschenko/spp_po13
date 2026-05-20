"""Модуль корзины покупок с применением скидок и купонов."""

import requests

COUPONS = {"SAVE10": 10, "HALF": 50}


class Cart:
    """Корзина покупок."""

    def __init__(self):
        """Инициализация корзины."""
        self.items = []

    def add_item(self, name, price):
        """Добавить товар в корзину."""
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": name, "price": price})

    def total(self):
        """Посчитать общую сумму корзины."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, discount_percent):
        """Применить скидку ко всем товарам."""
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Скидка должна быть от 0 до 100 процентов")

        for item in self.items:
            item["price"] *= (100 - discount_percent) / 100


def log_purchase(item):
    """Отправить данные о покупке на сервер."""
    response = requests.post(
        "https://example.com/log",
        json=item,
        timeout=30
    )
    response.raise_for_status()
    return response


def apply_coupon(cart, coupon_code):
    """Применить купон к корзине."""
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:
        raise ValueError("Invalid coupon")
