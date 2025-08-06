from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud import book as book_crud
from app.schemas.book import BookCreate, BookRead

router = APIRouter(prefix="/books", tags=["books"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BookRead)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return book_crud.create_book(db, book)

@router.get("/", response_model=list[BookRead])
def list_books(db: Session = Depends(get_db)):
    return book_crud.list_books(db)

@router.post("/{book_id}/borrow/{user_id}", response_model=BookRead)
def borrow(book_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        return book_crud.borrow_book(db, book_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{book_id}/return/{user_id}", response_model=BookRead)
def return_book(book_id: int, user_id: int, db: Session = Depends(get_db)):
    try:
        return book_crud.return_book(db, book_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
