"""Pydantic схемы для валидации."""
from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorCreate(BaseModel):
    """Схема создания автора."""
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    country: Optional[str] = None


class AuthorResponse(AuthorCreate):
    """Схема ответа с автором."""
    id: int

    class Config:  # pylint: disable=R0903
        """Настройки схемы."""
        from_attributes = True


class GenreCreate(BaseModel):
    """Схема создания жанра."""
    name: str
    description: Optional[str] = None


class GenreResponse(GenreCreate):
    """Схема ответа с жанром."""
    id: int

    class Config:  # pylint: disable=R0903
        """Настройки схемы."""
        from_attributes = True


class BookCreate(BaseModel):
    """Схема создания книги."""
    title: str
    author_id: int
    genre_id: int
    year: Optional[int] = None
    isbn: Optional[str] = None
    total_copies: int = 1
    price: float = 0


class BookResponse(BookCreate):
    """Схема ответа с книгой."""
    id: int
    available_copies: int

    class Config:  # pylint: disable=R0903
        """Настройки схемы."""
        from_attributes = True


class ReaderCreate(BaseModel):
    """Схема создания читателя."""
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None


class ReaderResponse(ReaderCreate):
    """Схема ответа с читателем."""
    id: int
    registration_date: date

    class Config:  # pylint: disable=R0903
        """Настройки схемы."""
        from_attributes = True


class LoanCreate(BaseModel):
    """Схема создания выдачи книги."""
    book_id: int
    reader_id: int
    due_date: date


class LoanResponse(BaseModel):
    """Схема ответа с выдачей книги."""
    id: int
    book_id: int
    reader_id: int
    loan_date: date
    due_date: date
    return_date: Optional[date]
    is_returned: bool

    class Config:  # pylint: disable=R0903
        """Настройки схемы."""
        from_attributes = True
