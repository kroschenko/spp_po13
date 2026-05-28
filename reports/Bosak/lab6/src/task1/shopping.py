"""Shopping cart module."""

import requests


class Cart:
    """Shopping cart class."""

    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        """Add item to cart."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self):
        """Calculate total price."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, percent):
        """Apply discount percentage to all items."""
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        factor = (100 - percent) / 100
        for item in self.items:
            item["price"] = round(item["price"] * factor, 2)


def log_purchase(item):
    """Log purchase to external service."""
    requests.post("https://example.com/log", json=item, timeout=5)


coupons = {"SAVE10": 10, "HALF": 50}


def apply_coupon(cart, coupon_code):
    """Apply coupon code to cart."""
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
