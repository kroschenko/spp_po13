class Abiturient:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)

    def avg_grade(self):
        return sum(self.grades) / len(self.grades) if self.grades else 0

    def is_admitted(self, passing_score=60):
        return self.avg_grade() >= passing_score


class Faculty:
    def __init__(self, name):
        self.name = name
        self.abiturients = []

    def register(self, abiturient):
        self.abiturients.append(abiturient)


def main():
    faculty = Faculty(input("Faculty name: "))
    num = int(input("Number of abiturients: "))

    for _ in range(num):
        name = input("Abiturient name: ")
        ab = Abiturient(name)
        faculty.register(ab)

        exam_count = int(input(f"Number of exams for {name}: "))
        for _ in range(exam_count):
            exam_name = input("Exam name: ")
            teacher = input("Teacher: ")
            grade = float(input("Grade: "))
            ab.add_grade(grade)

    print("\nResults:")
    for ab in faculty.abiturients:
        print(f"{ab.name}: average = {ab.avg_grade():.2f}, admitted: {ab.is_admitted()}")


if __name__ == "__main__":
    main()
