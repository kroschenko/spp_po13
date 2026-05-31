import requests


class Item:
    def __init__(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.name = name
        self.price = price


class Cart:
    def __init__(self):
        self.items = []
        self.discount_percent = 0

    def add_item(self, item):
        self.items.append(item)

    def total(self):
        subtotal = sum(item.price for item in self.items)
        return subtotal * (1 - self.discount_percent / 100)

    def apply_discount(self, percent):
        if percent < 0 or percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        self.discount_percent = percent


coupons = {"SAVE10": 10, "HALF": 50}


def apply_coupon(cart, coupon_code):
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")


def log_purchase(item):
    requests.post("https://example.com/log", json={"name": item.name, "price": item.price})
