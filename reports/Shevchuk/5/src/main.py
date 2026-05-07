"""FastAPI application for educational institutions database."""

from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import Base, SESSION_LOCAL, engine
from .models import Course, Department, EducationalInstitution, Enrollment, Program, Student
from .schemas import (
    CourseCreate,
    CourseResponse,
    DepartmentCreate,
    DepartmentResponse,
    EducationalInstitutionCreate,
    EducationalInstitutionResponse,
    EnrollmentCreate,
    EnrollmentResponse,
    ProgramCreate,
    ProgramResponse,
    StudentCreate,
    StudentResponse,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Educational Institutions API")


def get_db() -> Generator[Session, None, None]:
    """Provide database session."""
    db = SESSION_LOCAL()
    try:
        yield db
    finally:
        db.close()


@app.post("/institutions/", response_model=EducationalInstitutionResponse)
def create_institution(
    institution: EducationalInstitutionCreate,
    db: Session = Depends(get_db),
) -> EducationalInstitution:
    """Create educational institution."""
    new_item = EducationalInstitution(**institution.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/institutions/", response_model=list[EducationalInstitutionResponse])
def get_institutions(db: Session = Depends(get_db)) -> list[EducationalInstitution]:
    """Get all educational institutions."""
    return db.query(EducationalInstitution).all()


@app.put("/institutions/{institution_id}", response_model=EducationalInstitutionResponse)
def update_institution(
    institution_id: int,
    institution: EducationalInstitutionCreate,
    db: Session = Depends(get_db),
) -> EducationalInstitution:
    """Update educational institution."""
    found_item = db.query(EducationalInstitution).filter(EducationalInstitution.id == institution_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    for key, value in institution.model_dump().items():
        setattr(found_item, key, value)

    db.commit()
    db.refresh(found_item)
    return found_item


@app.delete("/institutions/{institution_id}")
def delete_institution(
    institution_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete educational institution."""
    found_item = db.query(EducationalInstitution).filter(EducationalInstitution.id == institution_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    db.delete(found_item)
    db.commit()
    return {"message": "Institution deleted"}


@app.post("/departments/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
) -> Department:
    """Create department."""
    institution = (
        db.query(EducationalInstitution).filter(EducationalInstitution.id == department.institution_id).first()
    )
    if institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    new_item = Department(**department.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/departments/", response_model=list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)) -> list[Department]:
    """Get all departments."""
    return db.query(Department).all()


@app.put("/departments/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    department: DepartmentCreate,
    db: Session = Depends(get_db),
) -> Department:
    """Update department."""
    found_item = db.query(Department).filter(Department.id == department_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Department not found")

    for key, value in department.model_dump().items():
        setattr(found_item, key, value)

    db.commit()
    db.refresh(found_item)
    return found_item


@app.delete("/departments/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete department."""
    found_item = db.query(Department).filter(Department.id == department_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Department not found")

    db.delete(found_item)
    db.commit()
    return {"message": "Department deleted"}


@app.post("/programs/", response_model=ProgramResponse)
def create_program(
    program: ProgramCreate,
    db: Session = Depends(get_db),
) -> Program:
    """Create educational program."""
    department = db.query(Department).filter(Department.id == program.department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    new_item = Program(**program.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/programs/", response_model=list[ProgramResponse])
def get_programs(db: Session = Depends(get_db)) -> list[Program]:
    """Get all educational programs."""
    return db.query(Program).all()


@app.put("/programs/{program_id}", response_model=ProgramResponse)
def update_program(
    program_id: int,
    program: ProgramCreate,
    db: Session = Depends(get_db),
) -> Program:
    """Update educational program."""
    found_item = db.query(Program).filter(Program.id == program_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Program not found")

    for key, value in program.model_dump().items():
        setattr(found_item, key, value)

    db.commit()
    db.refresh(found_item)
    return found_item


@app.delete("/programs/{program_id}")
def delete_program(
    program_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete educational program."""
    found_item = db.query(Program).filter(Program.id == program_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Program not found")

    db.delete(found_item)
    db.commit()
    return {"message": "Program deleted"}


@app.post("/students/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
) -> Student:
    """Create student."""
    program = db.query(Program).filter(Program.id == student.program_id).first()
    if program is None:
        raise HTTPException(status_code=404, detail="Program not found")

    new_item = Student(**student.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/students/", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)) -> list[Student]:
    """Get all students."""
    return db.query(Student).all()


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student: StudentCreate,
    db: Session = Depends(get_db),
) -> Student:
    """Update student."""
    found_item = db.query(Student).filter(Student.id == student_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student.model_dump().items():
        setattr(found_item, key, value)

    db.commit()
    db.refresh(found_item)
    return found_item


@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete student."""
    found_item = db.query(Student).filter(Student.id == student_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(found_item)
    db.commit()
    return {"message": "Student deleted"}


@app.post("/courses/", response_model=CourseResponse)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
) -> Course:
    """Create course."""
    department = db.query(Department).filter(Department.id == course.department_id).first()
    if department is None:
        raise HTTPException(status_code=404, detail="Department not found")

    new_item = Course(**course.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/courses/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)) -> list[Course]:
    """Get all courses."""
    return db.query(Course).all()


@app.put("/courses/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course: CourseCreate,
    db: Session = Depends(get_db),
) -> Course:
    """Update course."""
    found_item = db.query(Course).filter(Course.id == course_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in course.model_dump().items():
        setattr(found_item, key, value)

    db.commit()
    db.refresh(found_item)
    return found_item


@app.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete course."""
    found_item = db.query(Course).filter(Course.id == course_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(found_item)
    db.commit()
    return {"message": "Course deleted"}


@app.post("/enrollments/", response_model=EnrollmentResponse)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
) -> Enrollment:
    """Create enrollment."""
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")

    new_item = Enrollment(**enrollment.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/enrollments/", response_model=list[EnrollmentResponse])
def get_enrollments(db: Session = Depends(get_db)) -> list[Enrollment]:
    """Get all enrollments."""
    return db.query(Enrollment).all()


@app.put("/enrollments/{enrollment_id}", response_model=EnrollmentResponse)
def update_enrollment(
    enrollment_id: int,
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
) -> Enrollment:
    """Update enrollment."""
    found_item = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    for key, value in enrollment.model_dump().items():
        setattr(found_item, key, value)

    db.commit()
    db.refresh(found_item)
    return found_item


@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete enrollment."""
    found_item = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if found_item is None:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(found_item)
    db.commit()
    return {"message": "Enrollment deleted"}
