from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date

# Строка подключения к LocalDB
DATABASE_URL = "mssql+pyodbc://@(localdb)\\MSSQLLocalDB/DeaneryDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


# Модели
class Group(Base):
    __tablename__ = "Groups"
    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(20), nullable=False, unique=True)
    course = Column(Integer)
    faculty = Column(String(100), nullable=False)

    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "Students"
    student_id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    birth_date = Column(Date, nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    group_id = Column(Integer, ForeignKey("Groups.group_id"))

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Teacher(Base):
    __tablename__ = "Teachers"
    teacher_id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=False)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    degree = Column(String(50))
    phone = Column(String(20))

    subjects = relationship("Subject", back_populates="teacher")


class Subject(Base):
    __tablename__ = "Subjects"
    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String(100), nullable=False)
    hours = Column(Integer)
    teacher_id = Column(Integer, ForeignKey("Teachers.teacher_id"))

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "Grades"
    grade_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("Students.student_id"))
    subject_id = Column(Integer, ForeignKey("Subjects.subject_id"))
    grade = Column(Integer)
    grade_date = Column(Date, default=date.today)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
