class Student:

    def __init__(self, name: str):
        self.name = name
        self.lab_status = {}
        self.exam_grade = None

    def get_name(self) -> str:
        return self.name

    def get_lab_status(self, lab_number: int) -> str:
        return self.lab_status.get(lab_number, "not checked")


class Professor:

    _instance = None
    _students = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._students is None:
            self._students = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def check_lab(self, student: Student, lab_number: int):
        if student not in self._students:
            self._students.append(student)
        student.lab_status[lab_number] = "checked"
        print(f"Professor: work {lab_number} of {student.get_name()} checked")

    def provide_consultation(self, student: Student, topic: str):
        print(f"Professor: consultation with {student.get_name()} on {topic}")

    def take_exam(self, student: Student):
        print(f"Professor: exam taken from {student.get_name()}")

    def set_mark(self, student: Student, grade: int):
        student.exam_grade = grade
        print(f"Professor: {student.get_name()} got mark {grade}")

    def provide_lecture(self, topic: str):
        print(f"Professor: lecture on {topic}")
        for student in self._students:
            print(f"  {student.get_name()} attended")


PROF1 = Professor.get_instance()
PROF2 = Professor.get_instance()

print(f"Same instance? {PROF1 is PROF2}")

STUDENT1 = Student("Ivanov")
STUDENT2 = Student("Petrov")

PROF1.check_lab(STUDENT1, 1)
PROF1.provide_consultation(STUDENT2, "OOP")
PROF1.take_exam(STUDENT1)
PROF1.set_mark(STUDENT1, 5)
PROF1.provide_lecture("Design Patterns")
