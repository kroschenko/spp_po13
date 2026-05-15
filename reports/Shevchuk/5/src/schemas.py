"""Pydantic schemas for educational institutions database."""

# pylint: disable=too-few-public-methods

from datetime import date

from pydantic import BaseModel, ConfigDict


class EducationalInstitutionCreate(BaseModel):
    """Schema for creating an educational institution."""

    name: str
    city: str
    address: str
    institution_type: str


class EducationalInstitutionResponse(EducationalInstitutionCreate):
    """Schema for educational institution response."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class DepartmentCreate(BaseModel):
    """Schema for creating a department."""

    institution_id: int
    name: str
    phone: str


class DepartmentResponse(DepartmentCreate):
    """Schema for department response."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class ProgramCreate(BaseModel):
    """Schema for creating a program."""

    department_id: int
    name: str
    degree_level: str
    duration_years: int


class ProgramResponse(ProgramCreate):
    """Schema for program response."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class StudentCreate(BaseModel):
    """Schema for creating a student."""

    program_id: int
    full_name: str
    birth_date: date
    email: str
    enrollment_year: int


class StudentResponse(StudentCreate):
    """Schema for student response."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class CourseCreate(BaseModel):
    """Schema for creating a course."""

    department_id: int
    name: str
    credits: int
    semester: int


class CourseResponse(CourseCreate):
    """Schema for course response."""

    id: int
    model_config = ConfigDict(from_attributes=True)


class EnrollmentCreate(BaseModel):
    """Schema for creating an enrollment."""

    student_id: int
    course_id: int
    enrollment_date: date
    grade: str


class EnrollmentResponse(EnrollmentCreate):
    """Schema for enrollment response."""

    id: int
    model_config = ConfigDict(from_attributes=True)
