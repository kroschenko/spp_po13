from abc import ABC, abstractmethod

# Интерфейс цифровых часов
class DigitalClockInterface(ABC):
    @abstractmethod
    def get_time_string(self):
        pass

    @abstractmethod
    def set_time(self, hours, minutes, seconds):
        pass

# Класс стрелочных часов
class AnalogClock:
    def __init__(self):
        self.second_angle = 0
        self.minute_angle = 0
        self.hour_angle = 0

    def tick(self):
        """Проходит 1 секунда"""
        self.second_angle = (self.second_angle + 6) % 360

        if self.second_angle == 0:
            self.minute_angle = (self.minute_angle + 6) % 360

            if self.minute_angle == 0:
                self.hour_angle = (self.hour_angle + 30) % 360

    def set_angles(self, hour_angle, minute_angle, second_angle):
        self.hour_angle = hour_angle % 360
        self.minute_angle = minute_angle % 360
        self.second_angle = second_angle % 360

    def get_angles(self):
        return self.hour_angle, self.minute_angle, self.second_angle

# Адаптер
class ClockAdapter(DigitalClockInterface):
    def __init__(self, analog_clock):
        self.clock = analog_clock

    def set_time(self, hours, minutes, seconds):
        """Преобразует время в углы"""
        self.clock.set_angles(
            hours * 30,
            minutes * 6,
            seconds * 6
        )

    def get_time_string(self):
        """Преобразует углы во время"""
        h_angle, m_angle, s_angle = self.clock.get_angles()

        hours = h_angle // 30
        minutes = m_angle // 6
        seconds = s_angle // 6

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def tick(self):
        self.clock.tick()

def main():
    print("ЧАСЫ")
    print("-" * 30)

    # Создаем часы
    analog_clock = AnalogClock()
    digital_clock = ClockAdapter(analog_clock)

    # Устанавливаем время
    print("Установка времени 10:30:45")
    digital_clock.set_time(10, 30, 45)

    # Проверяем
    print(f"Цифровое время: {digital_clock.get_time_string()}")
    h, m, s = analog_clock.get_angles()
    print(f"Углы стрелок: час {h}°, мин {m}°, сек {s}°")

    # Проходит 15 секунд
    print("\nПроходит 15 секунд...")
    for _ in range(15):
        digital_clock.tick()

    print(f"Текущее время: {digital_clock.get_time_string()}")
    h, m, s = analog_clock.get_angles()
    print(f"Углы стрелок: час {h}°, мин {m}°, сек {s}°")

if __name__ == "__main__":
    main()
