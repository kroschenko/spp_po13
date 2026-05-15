"""Простая корзина покупок для ЛР6."""

import requests

COUPONS = {"SAVE10": 10, "HALF": 50}


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": float(price)})

    def total(self):
        total_sum = 0.0
        for item in self.items:
            total_sum += item["price"]
        return total_sum

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be in [0, 100]")
        k = 1 - percent / 100
        for item in self.items:
            item["price"] = round(item["price"] * k, 2)


def log_purchase(item):
    requests.post("https://example.com/log", json=item, timeout=10)


def apply_coupon(cart, coupon_code):
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:
        raise ValueError("Invalid coupon")
