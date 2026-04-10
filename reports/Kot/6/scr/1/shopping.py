# shopping.py
class Cart:
    def __init__(self):
        self.items = []
        self.total = 0
        self.discount = 0

    def add_item(self, name, price):
        self.items.append({"name": name, "price": price})
        self.total += price

    def apply_discount(self, percent):
        """Apply discount in percent"""
        self.discount = percent
        self.total = self.total * (100 - percent) / 100

    def get_total(self):
        return self.total


# Move coupons to module level for easier testing
COUPONS = {"SAVE10": 10, "HALF": 50}


def apply_coupon(cart, coupon_code):
    if coupon_code in COUPONS:
        cart.apply_discount(COUPONS[coupon_code])
    else:

        raise ValueError("Invalid coupon")
