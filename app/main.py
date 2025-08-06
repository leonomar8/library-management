from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user, book

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
#app.include_router(user.router, prefix="/users", tags=["Users"])
#app.include_router(book.router, prefix="/books", tags=["Books"])

app.include_router(user.router)
app.include_router(book.router)
