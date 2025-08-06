from pydantic import BaseModel
from datetime import date
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    available: bool
    borrowed_by_id: Optional[int] = None
    due_date: Optional[date] = None

    class Config:
        from_attributes = True