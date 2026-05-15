"""SQLAlchemy models for educational institutions database."""

# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class EducationalInstitution(Base):
    """Educational institution table."""

    __tablename__ = "educational_institutions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    institution_type = Column(String(50), nullable=False)

    departments = relationship(
        "Department",
        back_populates="institution",
        cascade="all, delete",
    )


class Department(Base):
    """Department table."""

    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    institution_id = Column(
        Integer,
        ForeignKey("educational_institutions.id"),
        nullable=False,
    )
    name = Column(String(150), nullable=False)
    phone = Column(String(30), nullable=False)

    institution = relationship("EducationalInstitution", back_populates="departments")
    programs = relationship(
        "Program",
        back_populates="department",
        cascade="all, delete",
    )
    courses = relationship(
        "Course",
        back_populates="department",
        cascade="all, delete",
    )


class Program(Base):
    """Program table."""

    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    name = Column(String(150), nullable=False)
    degree_level = Column(String(50), nullable=False)
    duration_years = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="programs")
    students = relationship(
        "Student",
        back_populates="program",
        cascade="all, delete",
    )


class Student(Base):
    """Student table."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    full_name = Column(String(150), nullable=False)
    birth_date = Column(Date, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    enrollment_year = Column(Integer, nullable=False)

    program = relationship("Program", back_populates="students")
    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete",
    )


class Course(Base):
    """Course table."""

    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    name = Column(String(150), nullable=False)
    credits = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    department = relationship("Department", back_populates="courses")
    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete",
    )


class Enrollment(Base):
    """Enrollment table."""

    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    grade = Column(String(10), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
