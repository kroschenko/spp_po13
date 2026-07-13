class Account:
    def get_discount(self):
        return 0

    def get_benefits(self):
        return []

    def get_name(self):
        return "Базовая"


class BaseAccount(Account):
    def get_discount(self):
        return 0

    def get_benefits(self):
        return ["Просмотр книг"]

    def get_name(self):
        return "Базовая"


class SilverLevel(Account):
    def __init__(self, account):
        self.account = account

    def get_discount(self):
        return self.account.get_discount() + 5

    def get_benefits(self):
        benefits = self.account.get_benefits()
        benefits.append("Скидка 5%")
        benefits.append("Бесплатная доставка")
        return benefits

    def get_name(self):
        return f"{self.account.get_name()} + Серебряный"


class GoldLevel(Account):
    def __init__(self, account):
        self.account = account

    def get_discount(self):
        return self.account.get_discount() + 10

    def get_benefits(self):
        benefits = self.account.get_benefits()
        benefits.append("Скидка 10%")
        benefits.append("Бесплатная доставка за 1 час")
        benefits.append("Доступ к эксклюзивным книгам")
        benefits.append("Приоритетная поддержка")
        return benefits

    def get_name(self):
        return f"{self.account.get_name()} + Золотой"


def show_account_info(account):
    print(f"\n=== {account.get_name()} ===")
    print(f"Скидка: {account.get_discount()}%")
    print("Возможности:")
    for benefit in account.get_benefits():
        print(f"  - {benefit}")


if __name__ == "__main__":
    BASE = BaseAccount()
    show_account_info(BASE)
    SILVER = SilverLevel(BASE)
    show_account_info(SILVER)
    GOLD = GoldLevel(SILVER)
    show_account_info(GOLD)

    print("\n=== Покупатель заказал книгу ===")
    BOOK_PRICE = 1000
    FINAL_PRICE = BOOK_PRICE - (BOOK_PRICE * GOLD.get_discount() / 100)
    print(f"Цена книги: {BOOK_PRICE} руб.")
    print(f"Скидка: {GOLD.get_discount()}%")
    print(f"Итого: {FINAL_PRICE} руб.")
