"""CRUD операции с базой данных."""
from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas


# AUTHORS
def get_author(db: Session, author_id: int):
    """Получение автора по ID."""
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    """Получение списка авторов."""
    return db.query(models.Author).offset(skip).limit(limit).all()


def create_author(db: Session, author: schemas.AuthorCreate):
    """Создание автора."""
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: schemas.AuthorCreate):
    """Обновление автора."""
    db_author = get_author(db, author_id)
    if db_author:
        for key, value in author.model_dump().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int):
    """Удаление автора."""
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
        return True
    return False


# GENRES
def get_genres(db: Session):
    """Получение списка жанров."""
    return db.query(models.Genre).all()


def create_genre(db: Session, genre: schemas.GenreCreate):
    """Создание жанра."""
    db_genre = models.Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def delete_genre(db: Session, genre_id: int):
    """Удаление жанра."""
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if genre:
        db.delete(genre)
        db.commit()
        return True
    return False


# BOOKS
def get_book(db: Session, book_id: int):
    """Получение книги по ID."""
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: Optional[int] = None):
    """Получение списка книг с фильтрацией по автору."""
    query = db.query(models.Book)
    if author_id:
        query = query.filter(models.Book.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    """Создание книги."""
    db_book = models.Book(**book.model_dump(), available_copies=book.total_copies)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookCreate):
    """Обновление книги."""
    db_book = get_book(db, book_id)
    if db_book:
        for key, value in book.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    """Удаление книги."""
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False


# READERS
def get_reader(db: Session, reader_id: int):
    """Получение читателя по ID."""
    return db.query(models.Reader).filter(models.Reader.id == reader_id).first()


def get_readers(db: Session):
    """Получение списка читателей."""
    return db.query(models.Reader).all()


def create_reader(db: Session, reader: schemas.ReaderCreate):
    """Создание читателя."""
    db_reader = models.Reader(**reader.model_dump())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader


def update_reader(db: Session, reader_id: int, reader: schemas.ReaderCreate):
    """Обновление читателя."""
    db_reader = get_reader(db, reader_id)
    if db_reader:
        for key, value in reader.model_dump().items():
            setattr(db_reader, key, value)
        db.commit()
        db.refresh(db_reader)
    return db_reader


def delete_reader(db: Session, reader_id: int):
    """Удаление читателя."""
    db_reader = get_reader(db, reader_id)
    if db_reader:
        db.delete(db_reader)
        db.commit()
        return True
    return False


# LOANS
def create_loan(db: Session, loan: schemas.LoanCreate):
    """Создание выдачи книги."""
    book = get_book(db, loan.book_id)
    if not book or book.available_copies < 1:
        return None

    db_loan = models.Loan(
        book_id=loan.book_id,
        reader_id=loan.reader_id,
        loan_date=date.today(),
        due_date=loan.due_date,
        is_returned=False
    )

    book.available_copies -= 1
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def get_loans(db: Session, reader_id: Optional[int] = None):
    """Получение списка выдач."""
    query = db.query(models.Loan)
    if reader_id:
        query = query.filter(models.Loan.reader_id == reader_id)
    return query.all()


def return_book(db: Session, loan_id: int):
    """Возврат книги."""
    loan = db.query(models.Loan).filter(models.Loan.id == loan_id).first()
    if not loan or loan.is_returned:
        return None

    loan.is_returned = True
    loan.return_date = date.today()

    book = get_book(db, loan.book_id)
    if book:
        book.available_copies += 1

    db.commit()
    return loan
