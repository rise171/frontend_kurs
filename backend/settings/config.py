from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: Optional[str] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "your_password"
    DB_NAME: str = "psychology_db"

    @property
    def DATABASE_URL_AUTO(self) -> str:
        """Автоматически собирает URL базы данных из компонентов"""
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Admin settings
    ADMIN_EMAIL: str = "admin@gmail.com"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()