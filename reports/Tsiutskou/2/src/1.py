class LimitedSet:
    def __init__(self, max_power, elements=None):
        self.max_power = max_power
        self.items = []
        if elements:
            for e in elements:
                self.add(e)

    def add(self, value):
        if value not in self.items and len(self.items) < self.max_power:
            self.items.append(float(value))
            return True
        return False

    def remove(self, value):
        if value in self.items:
            self.items.remove(value)
            return True
        return False

    def contains(self, value):
        return value in self.items

    def intersection(self, other):
        result = LimitedSet(min(self.max_power, other.max_power))
        for item in self.items:
            if item in other.items:
                result.add(item)
        return result

    def __str__(self):
        return "{" + ", ".join(str(x) for x in self.items) + "}"

    def __eq__(self, other):
        return set(self.items) == set(other.items)


# Создание множеств
s1 = LimitedSet(5, [1.5, 2.7, 3.2, 4.8])
s2 = LimitedSet(5, [2.7, 4.8, 6.1, 7.5])
print("Множество 1:", s1)
print("Множество 2:", s2)
# Проверка принадлежности
print(f"Содержит 2.7? {s1.contains(2.7)}")
# Добавление элемента
s1.add(5.9)
print("После добавления 5.9:", s1)
# Удаление элемента
s1.remove(1.5)
print("После удаления 1.5:", s1)
# Пересечение
s3 = s1.intersection(s2)
print("Пересечение:", s3)
# Сравнение
s4 = LimitedSet(5, [2.7, 4.8])
print(f"Равны? {s3 == s4}")
