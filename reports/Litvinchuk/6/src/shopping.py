"""Shopping cart module with discount, coupon, and logging support."""

import requests

COUPONS = {
    "SAVE10": 10,
    "HALF": 50,
}


class Cart:
    """Represents a shopping cart."""

    def __init__(self):
        """Initialize an empty cart."""
        self.items = []
        self.discount = 0

    def add_item(self, name, price):
        """Add an item to the cart."""
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self):
        """Calculate the total cart price with discount applied."""
        total_price = sum(item["price"] for item in self.items)
        return total_price * (1 - self.discount / 100)

    def apply_discount(self, percent):
        """Apply a percentage discount to the cart."""
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount = percent


def log_purchase(item):
    """Send purchase information to a remote logging service."""
    requests.post("https://example.com/log", json=item, timeout=5)


def apply_coupon(cart, coupon_code):
    """Apply a coupon discount to the cart."""
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:
        raise ValueError("Invalid coupon")
