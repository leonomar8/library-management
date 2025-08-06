from pydantic import BaseModel
from typing import List
from app.schemas.book import BookRead

class UserCreate(BaseModel):
    name: str

class UserRead(BaseModel):
    id: int
    name: str
    total_fines: int
    borrowed_books: List[BookRead] = []

    class Config:
        from_attributes = True
    