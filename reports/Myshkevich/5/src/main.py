"""FastAPI приложение Библиотека."""
from datetime import date
from typing import List, Optional

from fastapi import FastAPI, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import engine, get_db

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Библиотека")


# ГЛАВНАЯ
@app.get("/", response_class=HTMLResponse)
def root():
    """Главная страница."""
    return """
    <h1>Библиотека</h1>
    <ul>
        <li><a href="/authors">Авторы</a></li>
        <li><a href="/books">Книги</a></li>
        <li><a href="/readers">Читатели</a></li>
        <li><a href="/loans">Выдача книг</a></li>
    </ul>
    <hr>
    <h3>JSON API:</h3>
    <ul>
        <li><a href="/api/authors">/api/authors</a></li>
        <li><a href="/api/books">/api/books</a></li>
        <li><a href="/api/readers">/api/readers</a></li>
        <li><a href="/api/loans">/api/loans</a></li>
    </ul>
    """


# АВТОРЫ
@app.get("/authors", response_class=HTMLResponse)
def authors_page(db: Session = Depends(get_db)):
    """Страница управления авторами."""
    authors = crud.get_authors(db)

    html = "<h1>Авторы</h1><a href='/'>Назад</a><br><br>"

    # Форма добавления
    html += """
    <form method='post' action='/authors/add'>
        <input type='text' name='first_name' placeholder='Имя' required>
        <input type='text' name='last_name' placeholder='Фамилия' required>
        <input type='date' name='birth_date'>
        <input type='text' name='country' placeholder='Страна'>
        <button type='submit'>Добавить</button>
    </form>
    <br>
    <table border='1'>
        <tr><th>ID</th><th>Имя</th><th>Фамилия</th><th>Действия</th></tr>
    """

    for a in authors:
        html += f"""
        <tr>
            <td>{a.id}</td>
            <td>{a.first_name}</td>
            <td>{a.last_name}</td>
            <td>
                <form method='post' action='/authors/delete/{a.id}' style='display:inline'>
                    <button type='submit'>Удалить</button>
                </form>
            </td>
        </tr>
        """

    html += "</table>"
    return html


@app.post("/authors/add")
def add_author(  # pylint: disable=R0913,R0917
    first_name: str = Form(...),
    last_name: str = Form(...),
    birth_date: Optional[str] = Form(None),
    country: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Добавление автора."""
    author = schemas.AuthorCreate(
        first_name=first_name,
        last_name=last_name,
        birth_date=date.fromisoformat(birth_date) if birth_date else None,
        country=country
    )
    crud.create_author(db, author)
    return authors_page(db)


@app.post("/authors/delete/{author_id}")
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Удаление автора."""
    crud.delete_author(db, author_id)
    return authors_page(db)


# КНИГИ
@app.get("/books", response_class=HTMLResponse)
def books_page(db: Session = Depends(get_db)):
    """Страница управления книгами."""
    books = crud.get_books(db)
    authors = crud.get_authors(db)
    genres = crud.get_genres(db)

    html = "<h1>Книги</h1><a href='/'>Назад</a><br><br>"

    # Форма добавления
    html += "<form method='post' action='/books/add'>"
    html += "<input type='text' name='title' placeholder='Название' required>"
    html += "<select name='author_id' required><option value=''>Автор</option>"
    for a in authors:
        html += f"<option value='{a.id}'>{a.first_name} {a.last_name}</option>"
    html += "</select>"
    html += "<select name='genre_id' required><option value=''>Жанр</option>"
    for g in genres:
        html += f"<option value='{g.id}'>{g.name}</option>"
    html += "</select>"
    html += "<input type='number' name='year' placeholder='Год'>"
    html += "<input type='text' name='isbn' placeholder='ISBN'>"
    html += "<input type='number' name='total_copies' placeholder='Кол-во' value='1'>"
    html += "<input type='number' name='price' placeholder='Цена' step='0.01'>"
    html += "<button type='submit'>Добавить</button></form><br>"

    html += "<table border='1'>"
    html += "<tr><th>ID</th><th>Название</th><th>Автор</th><th>Доступно</th><th>Действия</th></tr>"
    for b in books:
        html += f"""
        <tr>
            <td>{b.id}</td>
            <td>{b.title}</td>
            <td>{b.author.first_name} {b.author.last_name}</td>
            <td>{b.available_copies}/{b.total_copies}</td>
            <td>
                <form method='post' action='/books/delete/{b.id}' style='display:inline'>
                    <button type='submit'>Удалить</button>
                </form>
            </td>
        </tr>
        """
    html += "</table>"
    return html


@app.post("/books/add")
def add_book(  # pylint: disable=R0913,R0917
    title: str = Form(...),
    author_id: int = Form(...),
    genre_id: int = Form(...),
    year: Optional[int] = Form(None),
    isbn: Optional[str] = Form(None),
    total_copies: int = Form(1),
    price: float = Form(0),
    db: Session = Depends(get_db)
):
    """Добавление книги."""
    book = schemas.BookCreate(
        title=title,
        author_id=author_id,
        genre_id=genre_id,
        year=year,
        isbn=isbn,
        total_copies=total_copies,
        price=price
    )
    crud.create_book(db, book)
    return books_page(db)


@app.post("/books/delete/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удаление книги."""
    crud.delete_book(db, book_id)
    return books_page(db)


# ЧИТАТЕЛИ
@app.get("/readers", response_class=HTMLResponse)
def readers_page(db: Session = Depends(get_db)):
    """Страница управления читателями."""
    readers = crud.get_readers(db)

    html = "<h1>Читатели</h1><a href='/'>Назад</a><br><br>"

    html += """
    <form method='post' action='/readers/add'>
        <input type='text' name='first_name' placeholder='Имя' required>
        <input type='text' name='last_name' placeholder='Фамилия' required>
        <input type='email' name='email' placeholder='Email' required>
        <input type='text' name='phone' placeholder='Телефон'>
        <input type='text' name='address' placeholder='Адрес'>
        <button type='submit'>Добавить</button>
    </form>
    <br>
    <table border='1'>
        <tr><th>ID</th><th>Имя</th><th>Фамилия</th><th>Email</th><th>Действия</th></tr>
    """

    for r in readers:
        html += f"""
        <tr>
            <td>{r.id}</td>
            <td>{r.first_name}</td>
            <td>{r.last_name}</td>
            <td>{r.email}</td>
            <td>
                <form method='post' action='/readers/delete/{r.id}' style='display:inline'>
                    <button type='submit'>Удалить</button>
                </form>
            </td>
        </tr>
        """

    html += "</table>"
    return html


@app.post("/readers/add")
def add_reader(  # pylint: disable=R0913,R0917
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Добавление читателя."""
    reader = schemas.ReaderCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address
    )
    crud.create_reader(db, reader)
    return readers_page(db)


@app.post("/readers/delete/{reader_id}")
def delete_reader(reader_id: int, db: Session = Depends(get_db)):
    """Удаление читателя."""
    crud.delete_reader(db, reader_id)
    return readers_page(db)


# ВЫДАЧА КНИГ
@app.get("/loans", response_class=HTMLResponse)
def loans_page(db: Session = Depends(get_db)):
    """Страница управления выдачей книг."""
    loans = crud.get_loans(db)
    books = crud.get_books(db)
    readers = crud.get_readers(db)

    html = "<h1>Выдача книг</h1><a href='/'>Назад</a><br><br>"

    html += "<form method='post' action='/loans/add'>"
    html += "<select name='book_id' required><option value=''>Книга</option>"
    for b in books:
        text = f"{b.title} (доступно: {b.available_copies})"
        html += f"<option value='{b.id}'>{text}</option>"
    html += "</select>"
    html += "<select name='reader_id' required><option value=''>Читатель</option>"
    for r in readers:
        html += f"<option value='{r.id}'>{r.first_name} {r.last_name}</option>"
    html += "</select>"
    html += "<input type='date' name='due_date' required>"
    html += "<button type='submit'>Выдать</button></form><br>"

    html += "<table border='1'>"
    html += "<tr><th>ID</th><th>Книга</th><th>Читатель</th><th>Статус</th><th>Действия</th></tr>"
    for loan in loans:
        status = "Возвращена" if loan.is_returned else "На руках"
        html += f"""
        <tr>
            <td>{loan.id}</td>
            <td>{loan.book.title}</td>
            <td>{loan.reader.first_name} {loan.reader.last_name}</td>
            <td>{status}</td>
            <td>
        """
        if not loan.is_returned:
            html += f"""
                <form method='post' action='/loans/return/{loan.id}' style='display:inline'>
                    <button type='submit'>Вернуть</button>
                </form>
            """
        html += "<tr></tr>"

    html += "</table>"
    return html


@app.post("/loans/add")
def add_loan(
    book_id: int = Form(...),
    reader_id: int = Form(...),
    due_date: str = Form(...),
    db: Session = Depends(get_db)
):
    """Добавление выдачи книги."""
    loan = schemas.LoanCreate(
        book_id=book_id,
        reader_id=reader_id,
        due_date=date.fromisoformat(due_date)
    )
    crud.create_loan(db, loan)
    return loans_page(db)


@app.post("/loans/return/{loan_id}")
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    """Возврат книги."""
    crud.return_book(db, loan_id)
    return loans_page(db)


# JSON API
@app.get("/api/authors", response_model=List[schemas.AuthorResponse])
def api_authors(db: Session = Depends(get_db)):
    """API: список авторов."""
    return crud.get_authors(db)


@app.get("/api/books", response_model=List[schemas.BookResponse])
def api_books(db: Session = Depends(get_db)):
    """API: список книг."""
    return crud.get_books(db)


@app.get("/api/readers", response_model=List[schemas.ReaderResponse])
def api_readers(db: Session = Depends(get_db)):
    """API: список читателей."""
    return crud.get_readers(db)


@app.get("/api/loans", response_model=List[schemas.LoanResponse])
def api_loans(db: Session = Depends(get_db)):
    """API: список выдач."""
    return crud.get_loans(db)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
