# test_cart.py
import pytest
from unittest.mock import patch, Mock
import requests


# Класс Cart (предполагаемая реализация)
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.items.append({"name": name, "price": price})

    def total(self):
        return sum(item["price"] for item in self.items)

    def apply_discount(self, discount_percent):
        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount must be between 0 and 100")
        discount_factor = (100 - discount_percent) / 100
        for item in self.items:
            item["price"] *= discount_factor


# Функция для логирования покупки
def log_purchase(item):
    requests.post("https://example.com/log", json=item)


# Функция для применения купона
def apply_coupon(cart, coupon_code):
    coupons = {"SAVE10": 10, "HALF": 50}
    if coupon_code in coupons:
        cart.apply_discount(coupons[coupon_code])
    else:
        raise ValueError("Invalid coupon")


# Фикстура для пустой корзины
@pytest.fixture
def empty_cart():
    return Cart()


# Фикстура для корзины с одним товаром
@pytest.fixture
def cart_with_apple(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    return empty_cart


# 1. Тесты добавления товара
def test_add_item_single(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["name"] == "Apple"
    assert empty_cart.items[0]["price"] == 10.0


def test_add_multiple_items(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    empty_cart.add_item("Orange", 15.0)
    assert len(empty_cart.items) == 3


def test_negative_price_raises_error(empty_cart):
    with pytest.raises(ValueError, match="Price cannot be negative"):
        empty_cart.add_item("Apple", -10.0)


def test_zero_price_allowed(empty_cart):
    empty_cart.add_item("Free Item", 0.0)
    assert len(empty_cart.items) == 1
    assert empty_cart.items[0]["price"] == 0.0


# 2. Тесты метода apply_discount с параметризацией
@pytest.mark.parametrize(
    "discount,expected_price",
    [
        (0, 10.0),  # 0% скидка
        (50, 5.0),  # 50% скидка
        (100, 0.0),  # 100% скидка
    ],
)
def test_apply_discount_valid(cart_with_apple, discount, expected_price):
    cart_with_apple.apply_discount(discount)
    assert cart_with_apple.items[0]["price"] == expected_price


@pytest.mark.parametrize("invalid_discount", [-10, -1, 101, 150])
def test_apply_discount_invalid_values(empty_cart, invalid_discount):
    empty_cart.add_item("Apple", 10.0)
    with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
        empty_cart.apply_discount(invalid_discount)


def test_apply_discount_on_multiple_items(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    empty_cart.apply_discount(50)
    assert empty_cart.items[0]["price"] == 5.0
    assert empty_cart.items[1]["price"] == 10.0


# 3. Тест вычисления общей стоимости
def test_total_empty_cart(empty_cart):
    assert empty_cart.total() == 0.0


def test_total_single_item(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    assert empty_cart.total() == 10.0


def test_total_multiple_items(empty_cart):
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    empty_cart.add_item("Orange", 15.0)
    assert empty_cart.total() == 45.0


def test_total_after_discount(cart_with_apple):
    cart_with_apple.add_item("Banana", 20.0)
    cart_with_apple.apply_discount(25)  # 25% скидка
    # Apple: 10 * 0.75 = 7.5, Banana: 20 * 0.75 = 15.0
    expected_total = 7.5 + 15.0
    assert cart_with_apple.total() == expected_total


# 4. Тесты с моком requests.post
def test_log_purchase_mock():
    test_item = {"name": "Apple", "price": 10.0}

    with patch("requests.post") as mock_post:
        # Настройка мока
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Вызов тестируемой функции
        log_purchase(test_item)

        # Проверка, что post был вызван с правильными параметрами
        mock_post.assert_called_once_with("https://example.com/log", json=test_item)


def test_log_purchase_with_different_items():
    items = [
        {"name": "Apple", "price": 10.0},
        {"name": "Banana", "price": 20.0},
        {"name": "Orange", "price": 15.0},
    ]

    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        for item in items:
            log_purchase(item)

        # Проверяем, что post вызывался для каждого товара
        assert mock_post.call_count == 3

        # Проверяем аргументы каждого вызова
        calls = mock_post.call_args_list
        assert calls[0][1]["json"] == {"name": "Apple", "price": 10.0}
        assert calls[1][1]["json"] == {"name": "Banana", "price": 20.0}
        assert calls[2][1]["json"] == {"name": "Orange", "price": 15.0}


# 5. Тесты для apply_coupon с моком словаря купонов
def test_apply_coupon_save10(empty_cart):
    empty_cart.add_item("Apple", 10.0)

    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.items[0]["price"] == 9.0  # 10% скидка


def test_apply_coupon_half(empty_cart):
    empty_cart.add_item("Apple", 10.0)

    apply_coupon(empty_cart, "HALF")
    assert empty_cart.items[0]["price"] == 5.0  # 50% скидка


def test_apply_coupon_invalid_code(empty_cart):
    empty_cart.add_item("Apple", 10.0)

    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon(empty_cart, "INVALID_CODE")


def test_apply_coupon_with_mocked_coupons(empty_cart):
    """Тест с использованием monkeypatch для подмены словаря купонов"""
    empty_cart.add_item("Apple", 10.0)

    # Создаем тестовый словарь купонов
    test_coupons = {"BIG50": 50, "MEGA75": 75}

    # Используем monkeypatch для замены словаря coupons внутри apply_coupon
    with patch("__main__.coupons", test_coupons):
        # Здесь мы не можем напрямую подменить локальную переменную,
        # поэтому покажем альтернативный подход
        pass


# Альтернативный подход с инъекцией зависимостей
def apply_coupon_with_dict(cart, coupon_code, coupons_dict):
    """Улучшенная версия с внедрением зависимостей"""
    if coupon_code in coupons_dict:
        cart.apply_discount(coupons_dict[coupon_code])
    else:
        raise ValueError("Invalid coupon")


def test_apply_coupon_dependency_injection(empty_cart):
    """Тест с внедрением зависимостей для словаря купонов"""
    empty_cart.add_item("Apple", 10.0)

    test_coupons = {"BIG50": 50, "MEGA75": 75}

    # Тестируем с существующим купоном
    apply_coupon_with_dict(empty_cart, "BIG50", test_coupons)
    assert empty_cart.items[0]["price"] == 5.0

    # Создаем новую корзину для следующего теста
    new_cart = Cart()
    new_cart.add_item("Apple", 10.0)

    # Тестируем с несуществующим купоном
    with pytest.raises(ValueError, match="Invalid coupon"):
        apply_coupon_with_dict(new_cart, "INVALID", test_coupons)


# Тест с использованием monkeypatch
def test_apply_coupon_monkeypatch(empty_cart, monkeypatch):
    """Тест с использованием monkeypatch для замены словаря"""
    empty_cart.add_item("Apple", 10.0)

    # Подменяем глобальный словарь coupons
    monkeypatch.setitem(__builtins__, "coupons", {"SUPER50": 50, "MICRO10": 10})

    # В реальном коде пришлось бы использовать import module
    # и monkeypatch.setattr(module, 'coupons', ...)

    # Демонстрируем концепцию с локальным словарем
    local_coupons = {"SUPER50": 50}
    apply_coupon_with_dict(empty_cart, "SUPER50", local_coupons)
    assert empty_cart.items[0]["price"] == 5.0


# Комплексные тесты
def test_full_shopping_workflow(empty_cart):
    """Полный сценарий покупки"""
    # Добавляем товары
    empty_cart.add_item("Apple", 10.0)
    empty_cart.add_item("Banana", 20.0)
    assert len(empty_cart.items) == 2

    # Проверяем общую стоимость
    assert empty_cart.total() == 30.0

    # Применяем скидку
    empty_cart.apply_discount(10)
    assert empty_cart.total() == 27.0

    # Применяем купон
    apply_coupon(empty_cart, "SAVE10")
    assert empty_cart.total() == 24.3  # 27 * 0.9


def test_error_handling_comprehensive(empty_cart):
    """Тестирование различных ошибочных ситуаций"""
    # Отрицательная цена
    with pytest.raises(ValueError):
        empty_cart.add_item("Invalid", -5.0)

    # Невалидная скидка
    empty_cart.add_item("Test", 10.0)
    with pytest.raises(ValueError):
        empty_cart.apply_discount(-10)

    with pytest.raises(ValueError):
        empty_cart.apply_discount(110)

    # Невалидный купон
    with pytest.raises(ValueError):
        apply_coupon(empty_cart, "NONEXISTENT")
