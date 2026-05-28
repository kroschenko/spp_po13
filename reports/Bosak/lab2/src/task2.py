"""Module for admission system."""


class Abiturient:
    """Class representing an applicant."""

    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        """Add exam grade."""
        self.grades.append(grade)

    def avg_grade(self):
        """Calculate average grade."""
        return sum(self.grades) / len(self.grades) if self.grades else 0

    def is_admitted(self, passing_score=60):
        """Check if applicant is admitted."""
        return self.avg_grade() >= passing_score


class Faculty:
    """Class representing a faculty."""

    def __init__(self, name):
        self.name = name
        self.abiturients = []

    def register(self, abiturient):
        """Register an applicant."""
        self.abiturients.append(abiturient)

    def get_name(self):
        """Return faculty name."""
        return self.name


def main():
    """Main function to run admission system."""
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
            _ = (exam_name, teacher)

    print("\nResults:")
    for ab in faculty.abiturients:
        print(f"{ab.name}: average = {ab.avg_grade():.2f}, admitted: {ab.is_admitted()}")


if __name__ == "__main__":
    main()
