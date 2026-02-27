"""
2) Система Платежи. Клиент имеет Счет в банке и Кредитную Карту (КК).
Клиент может оплатить Заказ, сделать платеж на другой Счет, заблокировать
КК и аннулировать Счет. Администратор может заблокировать КК за
превышение кредита.
"""


class Client:
    def __init__(self, name, creditCard):
        self.name = name
        self.creditCard = creditCard

    def print(self):
        print(self.name)
        print(self.creditCard)

    def payForOrder(self, order):
        self.creditCard.pay(order)

    def transferMoney(self, account, amount):
        self.creditCard.transfer(account, amount)

    def blockKK(self, creditCard):
        creditCard.block()

    def nullAccount(self):
        self.creditCard.nullAccount()


class Card:
    def __init__(self, account, number, status):
        self.account = account
        self.number = number
        self.status = status

    def getBalance(self):
        return self.account.getBalance()

    def pay(self, order):
        if order.cost <= self.getBalance() and order.status != "Paid" and self.status != "Blocked":
            self.account.pay(order.getCost())
            order.setStatus("Paid")
            print("Оплата прошла успешно")
        else:
            print("Операция не прошла!")

    def transfer(self, account, amount):
        if amount <= self.getBalance() and self.status != "Blocked":
            self.account.pay(amount)
            account.getMoney(amount)
            print("Перевод выполнен успешно")
        else:
            print("Операция не прошла!")

    def block(self):
        self.status = "Blocked"
        print("Карта заблокирована")

    def nullAccount(self):
        self.account.nullAccount()

    def transferMoney(self, account, amount):
        if amount <= self.getBalance() and self.status != "Blocked":
            self.account.pay(amount)
            account.getMoney(amount)
        else:
            print("Операция не прошла!")


class Order:
    def __init__(self, cost, status="Waiting"):
        self.cost = cost
        self.status = status

    def print(self):
        print(self.status)

    def setStatus(self, status):
        self.status = status

    def getCost(self):
        return self.cost





class BankAccount:
    def __init__(self, owner, creditcard, balance):
        self.owner = owner
        self.creditcard = creditcard
        self.balance = balance

    def getBalance(self):
        return self.balance

    def setBalance(self, balance):
        self.balance = balance

    def pay(self, amount):
        self.setBalance(self.balance - amount)
        if self.balance < 0:
            self.creditcard.block()
            print("Карта заблокирована из-за отрицательного баланса")

    def getMoney(self, amount):
        self.setBalance(self.balance + amount)

    def nullAccount(self):
        self.balance = 0
        print("Счет аннулирован")


class Administrator(Client):
    def __init__(self,name,credit_card=None):
        Client.__init__(self,name,credit_card)
    def blockKK(self, creditCard):
        creditCard.block()
        print(f"Администратор {self.name} заблокировал карту")


if __name__ == '__main__':
    bank_account = BankAccount("Иван Петров", None, 5000)
    credit_card = Card(bank_account, "4276-1234-5678-9012", "Active")
    bank_account.creditcard = credit_card

    client = Client("Иван Петров", credit_card)
    admin = Administrator("Петр Сидоров")

    print(f"Клиент: {client.name}")
    print(f"Номер карты: {credit_card.number}")
    print(f"Статус карты: {credit_card.status}")
    print(f"Баланс счета: {bank_account.getBalance()}")
    print(f"Баланс карты: {credit_card.getBalance()}")

    order1 = Order(2000, "Waiting")
    order2 = Order(4000, "Waiting")
    order3 = Order(1500, "Waiting")

    print(f"Заказ 1: сумма {order1.cost}, статус {order1.status}")
    print(f"Заказ 2: сумма {order2.cost}, статус {order2.status}")
    print(f"Заказ 3: сумма {order3.cost}, статус {order3.status}")

    client.payForOrder(order1)
    print(f"Статус заказа: {order1.status}")
    print(f"Баланс после оплаты: {bank_account.getBalance()}")

    client.payForOrder(order2)
    print(f"Статус заказа: {order2.status}")
    print(f"Баланс после оплаты: {bank_account.getBalance()}")
    print(f"Статус карты: {credit_card.status}")


    other_account = BankAccount("Петр Иванов", None, 1000)
    print(f"Баланс счета {other_account.owner} до перевода: {other_account.getBalance()}")

    client.transferMoney(other_account, 500)
    print(f"Баланс счета {client.name} после перевода: {bank_account.getBalance()}")
    print(f"Баланс счета {other_account.owner} после перевода: {other_account.getBalance()}")

    client.blockKK(credit_card)
    print(f"Статус карты: {credit_card.status}")

    client.payForOrder(order3)
    print(f"Статус заказа: {order3.status}")
    print(f"Баланс не изменился: {bank_account.getBalance()}")

    new_account = BankAccount("Сергей", None, 3000)
    new_card = Card(new_account, "5555-6666", "Active")
    new_account.creditcard = new_card
    print("Новая карта, статус: ",new_card.status)

    admin.blockKK(new_card)
    print("Статус карты после блокировки: ",new_card.status)

    print(f"Баланс до аннулирования: {bank_account.getBalance()}")
    client.nullAccount()
    print(f"Баланс после аннулирования: {bank_account.getBalance()}")
