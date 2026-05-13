"""Мини-библиотека покупок."""


class Requests:
    """Заглушка для имитации requests.post."""

    @staticmethod
    def post(url, json=None):
        """Имитирует отправку POST-запроса."""
        return {"url": url, "json": json}


requests = Requests()


class Cart:
    """Корзина покупок."""

    def __init__(self):
        """Создает пустую корзину."""
        self.items = []

    def add_item(self, name, price):
        """Добавляет товар в корзину."""
        if price < 0:
            raise ValueError("Price cannot be negative")

        self.items.append({"name": name, "price": price})

    def total(self):
        """Возвращает общую стоимость товаров."""
        return sum(item["price"] for item in self.items)

    def apply_discount(self, discount):
        """Применяет скидку к товарам."""
        if discount < 0 or discount > 100:
            raise ValueError("Invalid discount")

        for item in self.items:
            item["price"] = item["price"] * (1 - discount / 100)


COUPONS = {"SAVE10": 10, "HALF": 50}


def log_purchase(item):
    """Логирует покупку в удаленную систему."""
    requests.post("https://example.com/log", json=item)


def apply_coupon(cart, coupon_code):
    """Применяет купон к корзине."""
    if coupon_code not in COUPONS:
        raise ValueError("Invalid coupon")

    cart.apply_discount(COUPONS[coupon_code])
