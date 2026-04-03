"""Модуль для интерактивного выбора тура и формирования заказа."""

class TourPackage:
    """Класс для хранения информации о туре и его стоимости."""
    def __init__(self):
        self.transport = None
        self.accommodation = None
        self.meals = None
        self.excursions = []
        self.cost = 0

    def __str__(self):
        exc = ', '.join(self.excursions) if self.excursions else 'Нет'
        return (
            f"Тур:\n"
            f"  Проезд: {self.transport}\n"
            f"  Проживание: {self.accommodation}\n"
            f"  Питание: {self.meals}\n"
            f"  Экскурсии: {exc}\n"
            f"Итоговая стоимость: {self.cost} USD"
        )


class TourBuilder:
    """Пошаговое создание тура через паттерн Builder."""
    def __init__(self):
        """Создание пустого тура."""
        self.tour = TourPackage()

    def set_transport(self, option_transport: str, cost_transport: float):
        """Установить транспорт и добавить его стоимость."""
        self.tour.transport = option_transport
        self.tour.cost += cost_transport
        return self

    def set_accommodation(self, option_accommodation: str, cost_accommodation: float):
        """Установить проживание и добавить его стоимость."""
        self.tour.accommodation = option_accommodation
        self.tour.cost += cost_accommodation
        return self

    def set_meals(self, option_meals: str, cost_meals: float):
        """Установить питание и добавить его стоимость."""
        self.tour.meals = option_meals
        self.tour.cost += cost_meals
        return self

    def add_excursion(self, option_excursion: str, cost_excursion: float):
        """Добавить экскурсию и увеличить стоимость тура."""
        self.tour.excursions.append(option_excursion)
        self.tour.cost += cost_excursion
        return self

    def build(self):
        """Вернуть готовый объект TourPackage."""
        return self.tour


def choose_option(options_dict: dict, prompt_text: str):
    """Выбор опции пользователем по номеру."""
    print(prompt_text)
    for idx, (opt_name, opt_cost) in enumerate(options_dict.items(), 1):
        print(f"{idx}. {opt_name} — {opt_cost} USD")
    while True:
        user_choice = input("Выберите номер: ")
        if user_choice.isdigit() and 1 <= int(user_choice) <= len(options_dict):
            key = list(options_dict.keys())[int(user_choice) - 1]
            return key, options_dict[key]
        print("Неверный ввод. Попробуйте снова.")


if __name__ == "__main__":
    builder = TourBuilder()

    transport_options = {"Автобус": 100, "Поезд": 150, "Самолет": 300}
    selected_transport, selected_transport_cost = choose_option(transport_options, "Выберите транспорт:")
    builder.set_transport(selected_transport, selected_transport_cost)

    accommodation_options = {"Хостел": 50, "Отель 3*": 200, "Отель 5*": 500}
    selected_accommodation, selected_accommodation_cost = choose_option(accommodation_options, "Выберите проживание:")
    builder.set_accommodation(selected_accommodation, selected_accommodation_cost)

    meals_options = {"Без питания": 0, "Завтрак": 20, "Полный пансион": 50}
    selected_meals, selected_meals_cost = choose_option(meals_options, "Выберите питание:")
    builder.set_meals(selected_meals, selected_meals_cost)

    excursions_options = {"Музей": 30, "Экскурсия по городу": 40, "Выставка": 25}
    print("\nВыберите экскурсии (Enter без ввода — закончить):")
    while True:
        for idx, (exc_name, exc_cost) in enumerate(excursions_options.items(), 1):
            print(f"{idx}. {exc_name} — {exc_cost} USD")
        user_input = input("Введите номер экскурсии или Enter для окончания: ")
        if user_input == "":
            break
        if user_input.isdigit() and 1 <= int(user_input) <= len(excursions_options):
            selected_excursion = list(excursions_options.keys())[int(user_input) - 1]
            selected_excursion_cost = excursions_options[selected_excursion]
            builder.add_excursion(selected_excursion, selected_excursion_cost)
            print(f"Экскурсия {selected_excursion} добавлена.\n")
        else:
            print("Неверный ввод. Попробуйте снова.\n")

    tour = builder.build()
    print("\n--- Итоговый заказ ---")
    print(tour)
    