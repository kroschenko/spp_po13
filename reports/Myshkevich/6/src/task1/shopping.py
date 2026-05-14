"""Мини-библиотека для работы с корзиной покупок."""
import requests


class Cart:
    """Класс корзины покупок."""

    def __init__(self):
        """Инициализация пустой корзины."""
        self.items = []
        self.discount = 0

    def add_item(self, item: str, price: float):
        """
        Добавление товара в корзину.

        Args:
            item: Название товара
            price: Цена товара

        Raises:
            ValueError: Если цена отрицательная
        """
        if price < 0:
            raise ValueError("Цена не может быть отрицательной")
        self.items.append({"name": item, "price": price})

    def total(self) -> float:
        """
        Вычисление общей стоимости с учетом скидки.

        Returns:
            Общая стоимость
        """
        if not self.items:
            return 0.0
        subtotal = sum(item["price"] for item in self.items)
        return subtotal * (1 - self.discount / 100)

    def apply_discount(self, percent: float):
        """
        Применение скидки к корзине.

        Args:
            percent: Процент скидки (0-100)

        Raises:
            ValueError: Если процент скидки вне диапазона 0-100
        """
        if percent < 0 or percent > 100:
            raise ValueError("Скидка должна быть от 0 до 100 процентов")
        self.discount = percent


def log_purchase(item: dict):
    """
    Логирование покупки в удаленную систему.

    Args:
        item: Словарь с данными о покупке
    """
    # Добавлен timeout=5 чтобы избежать зависания
    requests.post("https://example.com/log", json=item, timeout=5)


def apply_coupon(cart: Cart, coupon_code: str):
    """
    Применение купона к корзине.

    Args:
        cart: Объект корзины
        coupon_code: Код купона

    Raises:
        ValueError: Если купон не найден
    """
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")
