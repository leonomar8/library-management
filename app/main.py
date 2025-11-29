from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import user, book

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Simple CORS for FrontEnd interaction: allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # <- allow any origin
    allow_credentials=False,
    allow_methods=["*"],   # <- allow GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],   # <- allow all headers
)

# Include routers
app.include_router(user.router)
app.include_router(book.router)
