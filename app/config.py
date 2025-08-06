from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Automatically reads from .env

    class Config:
        env_file = ".env"

settings = Settings()
