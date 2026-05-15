from abc import ABC, abstractmethod

class RemoteControl(ABC):

    @abstractmethod
    def activate_alarm(self):
        pass

    @abstractmethod
    def toggle_doors(self):
        pass

    @abstractmethod
    def start_engine(self):
        pass


class BasicRemote(RemoteControl):

    def __init__(self):
        self.range = 50
        self.feedback = False

    def activate_alarm(self):
        print(f"[BasicRemote] Сигнализация активирована (радиус {self.range} м)")

    def toggle_doors(self):
        print("[BasicRemote] Двери заблокированы/разблокированы (без подтверждения)")

    def start_engine(self):
        print("[BasicRemote] Двигатель запущен (только если ключ в салоне)")


class AdvancedRemote(RemoteControl):

    def __init__(self):
        self.range = 150
        self.feedback = True

    def activate_alarm(self):
        print(f"[AdvancedRemote] Сигнализация активирована с задержкой 5с (радиус {self.range} м)")
        if self.feedback:
            print("  -> Звуковой сигнал подтверждения")

    def toggle_doors(self):
        print("[AdvancedRemote] Двери открыты/закрыты (с миганием поворотников)")

    def start_engine(self):
        print("[AdvancedRemote] Двигатель запущен дистанционно (автозапуск)")


class PremiumRemote(RemoteControl):

    def __init__(self):
        self.range = 500
        self.feedback = True
        self.smartphone_integration = True

    def activate_alarm(self):
        print("[PremiumRemote] Сигнализация активирована с охраной периметра "
              f"(радиус {self.range} м)")
        if self.smartphone_integration:
            print("  -> Уведомление на смартфон: 'Сигнализация включена'")

    def toggle_doors(self):
        print("[PremiumRemote] Двери управляются бесключевым доступом "
              "(с подтверждением на смартфон)")

    def start_engine(self):
        print("[PremiumRemote] Двигатель запущен с климат-контролем (автозапуск по расписанию)")

class Car(ABC):

    def __init__(self, model: str, year: int, remote: RemoteControl):
        self.model = model
        self.year = year
        self.remote = remote
        self.engine_on = False
        self.doors_locked = True
        self.alarm_on = False

    @abstractmethod
    def get_info(self):
        pass

    def remote_activate_alarm(self):
        self.remote.activate_alarm()
        self.alarm_on = True

    def remote_toggle_doors(self):
        self.remote.toggle_doors()
        self.doors_locked = not self.doors_locked

    def remote_start_engine(self):
        self.remote.start_engine()
        self.engine_on = True

    def start_manually(self):
        print(f"[{self.model}] Двигатель запущен ключом")
        self.engine_on = True

    def lock_doors_manually(self):
        print(f"[{self.model}] Двери заблокированы вручную")
        self.doors_locked = True

class BMW(Car):
    def __init__(self, model: str, year: int, remote: RemoteControl):
        super().__init__(model, year, remote)
        self.brand = "BMW"

    def get_info(self):
        return f"{self.brand} {self.model} ({self.year})"

class Toyota(Car):
    def __init__(self, model: str, year: int, remote: RemoteControl):
        super().__init__(model, year, remote)
        self.brand = "Toyota"

    def get_info(self):
        return f"{self.brand} {self.model} ({self.year})"

class Lada(Car):
    def __init__(self, model: str, year: int, remote: RemoteControl):
        super().__init__(model, year, remote)
        self.brand = "Lada"

    def get_info(self):
        return f"{self.brand} {self.model} ({self.year})"


if __name__ == "__main__":
    basic = BasicRemote()
    advanced = AdvancedRemote()
    premium = PremiumRemote()

    bmw_x5 = BMW("X5", 2023, premium)
    toyota_camry = Toyota("Camry", 2022, advanced)
    lada_vesta = Lada("Vesta", 2021, basic)

    print("Тестирование BMW X5 с PremiumRemote")
    print(bmw_x5.get_info())
    bmw_x5.remote_activate_alarm()
    bmw_x5.remote_toggle_doors()
    bmw_x5.remote_start_engine()
    print()

    print("Тестирование Toyota Camry с AdvancedRemote")
    print(toyota_camry.get_info())
    toyota_camry.remote_activate_alarm()
    toyota_camry.remote_toggle_doors()
    toyota_camry.remote_start_engine()
    print()

    print("Тестирование Lada Vesta с BasicRemote")
    print(lada_vesta.get_info())
    lada_vesta.remote_activate_alarm()
    lada_vesta.remote_toggle_doors()
    lada_vesta.remote_start_engine()
    print()

    print("Меняем пульт у Lada на PremiumRemote")
    lada_vesta.remote = premium
    lada_vesta.remote_activate_alarm()
    lada_vesta.remote_start_engine()
