class State:
    def __init__(self, atm_object):
        self.atm = atm_object


class WaitState(State):
    def insert_card(self):
        print("Карта вставлена. Введите PIN")
        self.atm.state = self.atm.auth

    def enter_pin(self, _pin):
        print("Сначала вставьте карту")

    def withdraw(self, _amount):
        print("Сначала вставьте карту")

    def end(self):
        print("Нет сессии")


class AuthState(State):
    def insert_card(self):
        print("Карта уже есть")

    def enter_pin(self, pin):
        if pin == "1234":
            print("PIN верен")
            self.atm.state = self.atm.oper
        else:
            print("PIN неверен")
            self.atm.state = self.atm.wait

    def withdraw(self, _amount):
        print("Сначала введите PIN")

    def end(self):
        print("Сессия завершена")
        self.atm.state = self.atm.wait


class OperState(State):
    def insert_card(self):
        print("Карта уже есть")

    def enter_pin(self, _pin):
        print("PIN уже введен")

    def withdraw(self, amount):
        if amount > self.atm.cash:
            print("Нет денег в банкомате")
        elif amount > 10000:
            print("Лимит 10000 руб")
        else:
            self.atm.cash -= amount
            print(f"Выдано {amount} руб. Остаток: {self.atm.cash}")

        print("Заберите карту")
        self.atm.state = self.atm.wait

    def end(self):
        print("Заберите карту")
        self.atm.state = self.atm.wait


class BlockState(State):
    def insert_card(self):
        print("Банкомат заблокирован")

    def enter_pin(self, _pin):
        print("Банкомат заблокирован")

    def withdraw(self, _amount):
        print("Банкомат заблокирован")

    def end(self):
        print("Банкомат заблокирован")


class ATM:
    def __init__(self, cash):
        self.cash = cash
        self.wait = WaitState(self)
        self.auth = AuthState(self)
        self.oper = OperState(self)
        self.block = BlockState(self)
        self.state = self.wait

    def insert_card(self):
        self.state.insert_card()

    def enter_pin(self, pin):
        self.state.enter_pin(pin)

    def withdraw(self, amount):
        self.state.withdraw(amount)

    def end(self):
        self.state.end()


if __name__ == "__main__":
    ATM_MACHINE = ATM(50000)
    ATM_MACHINE.insert_card()
    ATM_MACHINE.enter_pin("1111")
    ATM_MACHINE.insert_card()
    ATM_MACHINE.enter_pin("1234")
    ATM_MACHINE.withdraw(15000)
    ATM_MACHINE.insert_card()
    ATM_MACHINE.enter_pin("1234")
    ATM_MACHINE.withdraw(5000)
