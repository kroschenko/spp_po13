"""Модели базы данных (5 таблиц)."""
from datetime import date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Author(Base):  # pylint: disable=R0903
    """Авторы."""
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date, nullable=True)
    country = Column(String(100), nullable=True)

    books = relationship("Book", back_populates="author")


class Genre(Base):  # pylint: disable=R0903
    """Жанры."""
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=True)

    books = relationship("Book", back_populates="genre")


class Book(Base):  # pylint: disable=R0903
    """Книги."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    year = Column(Integer, nullable=True)
    isbn = Column(String(20), unique=True, nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    price = Column(Numeric(10, 2), default=0)

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre", back_populates="books")
    loans = relationship("Loan", back_populates="book")


class Reader(Base):  # pylint: disable=R0903
    """Читатели."""
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    registration_date = Column(Date, default=date.today)

    loans = relationship("Loan", back_populates="reader")


class Loan(Base):  # pylint: disable=R0903
    """Выдача книг."""
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    loan_date = Column(Date, default=date.today, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    is_returned = Column(Boolean, default=False)

    book = relationship("Book", back_populates="loans")
    reader = relationship("Reader", back_populates="loans")
