# Стандартные импорты (должны быть первыми)
from datetime import date
from typing import List, Optional

# Затем сторонние библиотеки
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Затем локальные импорты (убрал неиспользуемые: engine, Base, Group, Subject)
from database import SessionLocal, Student, Teacher, Grade

app = FastAPI(title="Деканат API")


# Dependency для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic модели для данных
class StudentCreate(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    birth_date: date
    phone: Optional[str] = None
    email: Optional[str] = None
    group_id: int


class StudentResponse(StudentCreate):
    student_id: int

    class Config:
        orm_mode = True


# ============= Эндпойнты =============


# 1. ПОЛУЧЕНИЕ (SELECT) - список всех студентов
@app.get("/students", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


# 2. ДОБАВЛЕНИЕ (INSERT) - нового студента
@app.post("/students", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# 3. УДАЛЕНИЕ (DELETE) - студента по ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    db.delete(student)
    db.commit()
    return {"message": f"Студент {student_id} удален"}


# 4. МОДИФИКАЦИЯ (UPDATE) - обновление данных студента
@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student: StudentCreate, db: Session = Depends(get_db)
):
    db_student = db.query(Student).filter(Student.student_id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    for key, value in student.dict().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


# Дополнительные эндпойнты
@app.get("/groups/{group_id}/students")
def get_students_by_group(group_id: int, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.group_id == group_id).all()


@app.get("/teachers")
def get_teachers(db: Session = Depends(get_db)):
    return db.query(Teacher).all()


@app.post("/grades")
def add_grade(
    student_id: int, subject_id: int, grade: int, db: Session = Depends(get_db)
):
    new_grade = Grade(student_id=student_id, subject_id=subject_id, grade=grade)
    db.add(new_grade)
    db.commit()
    return {"message": "Оценка добавлена"}
