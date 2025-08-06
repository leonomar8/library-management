from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate
from datetime import date, timedelta

BORROW_LIMIT = 2
DUE_DAYS = 14
FINE_PER_DAY = 1

def create_book(db: Session, book: BookCreate):
    db_book = Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def list_books(db: Session):
    return db.query(Book).all()

def borrow_book(db: Session, book_id: int, user_id: int):
    book = db.query(Book).get(book_id)
    user = db.query(User).get(user_id)

    if not book or not user:
        raise ValueError("Book or User not found")

    if not book.available:
        raise ValueError("Book is already borrowed")

    if len(user.borrowed_books) >= BORROW_LIMIT:
        raise ValueError("Borrowing limit reached")

    book.available = False
    book.borrowed_by = user
    book.due_date = date.today() + timedelta(days=DUE_DAYS)
    db.commit()
    db.refresh(book)
    return book

def return_book(db: Session, book_id: int, user_id: int):
    book = db.query(Book).get(book_id)
    user = db.query(User).get(user_id)

    if not book or not user:
        raise ValueError("Book or User not found")

    if book.borrowed_by != user:
        raise ValueError("Book was not borrowed by this user")

    if date.today() > book.due_date:
        overdue_days = (date.today() - book.due_date).days
        user.total_fines += overdue_days * FINE_PER_DAY

    book.available = True
    book.borrowed_by = None
    book.borrowed_by_id = None
    book.due_date = None
    db.commit()
    db.refresh(book)
    return book
