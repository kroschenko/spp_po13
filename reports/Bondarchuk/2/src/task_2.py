Сверху в коментарии мое задание посмотри как я его реализовал и помоги мне использовать для наследия ABC 
также укажи на нетточности
"""1.2)"""
"""
2) Система Платежи. Клиент имеет Счет в банке и Кредитную Карту (КК).
Клиент может оплатить Заказ, сделать платеж на другой Счет, заблокировать
КК и аннулировать Счет. Администратор может заблокировать КК за
превышение кредита.
"""
class Client:

    def __init__(self, name,creditCard) :
        self.name = name
        self.creditCard = creditCard

    def print(self) :
        print(self.name)
        print(self.creditCard)

    def payForOrder(self,order) :
        self.creditCard.pay(order)

    def transferMoney(self,account, amount) :
        self.creditCard.transfer(account, amount)

    def blockKK(self,creditCard) :
        creditCard.block()

    def nullAccount(self) :
        self.creditCard.nullAccount()

class Card:
    def __init__(self,account,number,status) :
        self.account = account
        self.number = number
        self.status = status

    def getBalance(self) :
        return self.account.getBalance()

    def pay(self, order):
        if order.cost <= self.getBalance() and order.status != "Paid" and self.status!="Blocked":
            self.account.pay(order.getCost())
            order.setStatus("Paid")
        else:
            print("Операция не прошла!")

    def transfer(self, account, amount) :
        if amount <= self.creditCard.getBalance() and self.status!="Blocked":
            self.creditCard.transfer(account, amount)
        else:
            print("Операция не прошла!")

    def block(self) :
        self.status= "Blocked"

    def nullAccount(self) :
        self.account.nullAccount()

    def transferMoney(self, account, amount) :
        if amount <= self.getBalance() and self.status != "Blocked" and account.status!="Blocked":
            self.account.pay(amount)
            account.getMoney(amount)
        else:
            print("Операция не прошла!")

class Order:
    def __init__(self,cost,status="Waiting") :
        self.cost = cost
        self.number = status

    def print(self) :
        print(self.number)

    def setStatus(self, status) :
        self.status = status

    def getCost(self) :
        return self.cost

class Account:
    def __init__(self,owner) :
        self.owner = owner


class BankAccount:
    def __init__(self,owner,creditcard,balance) :
        self.owner = owner
        self.creditcard = creditcard
        self.balance = balance
    def getBalance(self) :
        return self.balance

    def setBalance(self,balance) :
        self.balance = balance

    def pay(self,amount) :
        self.setBalance(self,(self.balance-amount))
        if self.balance<0 :
            self.creditcard.block()

    def getMoney(self,amount) :
        self.setBalance(self, (self.balance + amount))

if __name__ == '__main__':
