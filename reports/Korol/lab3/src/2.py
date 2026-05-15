class AnalogClock:
    def __init__(self, hour_angle):
        self.hour_angle = hour_angle

    def get_angle(self):
        return self.hour_angle


class ClockAdapter:
    def __init__(self, analog_clock):
        self.analog_clock = analog_clock

    def get_time(self):
        hours = int(self.analog_clock.get_angle() / 30)

        if hours == 0:
            hours = 12

        return f"{hours}:00"


angle = int(input("Введите угол часовой стрелки: "))

clock = AnalogClock(angle)

adapter = ClockAdapter(clock)

print("Время:", adapter.get_time())
