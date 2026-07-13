class Subscriber:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.debt = 0
        self.services = []
        self.is_active = True

    def pay(self, amount):
        if amount <= self.debt:
            self.debt -= amount
            print(f"{self.name} оплатил {amount} руб. Остаток: {self.debt}")
        else:
            print(f"Оплачено {amount}, сдача {amount - self.debt}")
            self.debt = 0

    def make_call(self, minutes):
        cost = minutes * 0.2
        self.debt += cost
        print(f"Звонок {minutes} мин = {cost} руб.")

    def add_service(self, service_name, service_price):
        self.services.append(service_name)
        self.debt += service_price
        print(f"Добавлена услуга {service_name} ({service_price} руб.)")

    def remove_service(self, service_name):
        for s in self.services:
            if s == service_name:
                self.services.remove(s)
                print(f"Услуга {service_name} удалена")
                return
        print(f"Услуга {service_name} не найдена")


class Administrator:
    def __init__(self, name):
        self.name = name

    def change_number(self, subscriber, new_number):
        old = subscriber.phone_number
        subscriber.phone_number = new_number
        print(f"{self.name}: сменил номер {old} -> {new_number}")

    def disable(self, subscriber):
        if subscriber.debt > 0:
            subscriber.is_active = False
            print(f"{self.name}: отключил {subscriber.name} (долг {subscriber.debt} руб.)")

    def enable(self, subscriber):
        if subscriber.debt == 0:
            subscriber.is_active = True
            print(f"{self.name}: включил {subscriber.name}")


admin = Administrator("Иван")
sub = Subscriber("Петр", "123-45-67")
print(f"Абонент: {sub.name}, Номер: {sub.phone_number}\n")
sub.make_call(10)
sub.add_service("Интернет", 30)
sub.add_service("ТВ", 20)
print(f"\nДолг: {sub.debt} руб.")
print(f"Услуги: {sub.services}\n")
sub.pay(50)
print(f"Остаток долга: {sub.debt}\n")
admin.change_number(sub, "999-88-77")
admin.disable(sub)
print(f"Активен: {sub.is_active}")
