class Applicant:
    """Класс абитуриента с факультетом и экзаменами."""

    def __init__(self, full_name: str, faculty_name: str):
        self.name = full_name
        self.faculty = faculty_name
        self.exams = {}  # словарь экзамен: оценка

    def add_exam(self, exam_key: str, exam_value: float):
        """Добавление экзамена и оценки"""
        if 0 <= exam_value <= 100:
            self.exams[exam_key] = exam_value
        else:
            print("Ошибка: оценка должна быть от 0 до 100")

    def average_score(self) -> float:
        """Вычисление среднего балла"""
        if not self.exams:
            return 0
        return sum(self.exams.values()) / len(self.exams)

    def passed(self, threshold=60) -> bool:
        """Проверка, поступил ли абитуриент"""
        return self.average_score() >= threshold

    def __str__(self):
        exams_str = ", ".join(f"{k}: {v}" for k, v in self.exams.items())
        return (
            f"Абитуриент: {self.name}\n"
            f"Факультет: {self.faculty}\n"
            f"Экзамены: {exams_str}\n"
            f"Средний балл: {self.average_score():.2f}\n"
            f"Зачислен: {'Да' if self.passed() else 'Нет'}"
        )


# --- Ввод данных ---
user_name = input("Введите ФИО абитуриента: ")
user_faculty = input("Введите факультет: ")

applicant = Applicant(user_name, user_faculty)
print(f"\nАбитуриент {applicant.name} зарегистрирован на факультет {applicant.faculty}.\n")

# --- Ввод экзаменов ---
while True:
    exam_input = input("Введите название экзамена (или Enter для завершения): ")
    if exam_input == "":
        break
    try:
        mark_input = float(input(f"Введите оценку за {exam_input}: "))
        applicant.add_exam(exam_input, mark_input)
        print(f"Экзамен {exam_input} с оценкой {mark_input} добавлен.\n")
    except ValueError:
        print("Ошибка: оценка должна быть числом от 0 до 100.\n")

# --- Постепенный вывод информации ---
print("\n--- Итоговая информация об абитуриенте ---\n")
print(f"ФИО: {applicant.name}")
input("Нажмите Enter для продолжения...")
print(f"Факультет: {applicant.faculty}")
input("Нажмите Enter для продолжения...")
print("Сданные экзамены:")
for exam_name, exam_score in applicant.exams.items():
    print(f"  {exam_name}: {exam_score}")
input("Нажмите Enter для продолжения...")
print(f"Средний балл: {applicant.average_score():.2f}")
input("Нажмите Enter для продолжения...")
print(f"Зачислен: {'Да' if applicant.passed() else 'Нет'}")