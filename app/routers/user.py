from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas.user import UserCreate, UserRead
from app.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user.name)    
    if db_user:
        raise HTTPException(status_code=400, detail=f"A user with the name '{user.name}' already exists. Please choose a different name.")
    return user_crud.create_user(db, user)

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    return user_crud.get_users(db)