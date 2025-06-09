from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from settings.config import settings

# Формат URL для PostgreSQL:
# postgresql+asyncpg://username:password@host:port/database_name
DATABASE_URL = settings.DATABASE_URL or \
    "postgresql+asyncpg://postgres:your_password@localhost:5432/psychology_db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL запросов
    pool_size=20,  # Размер пула соединений
    max_overflow=10,  # Максимальное количество дополнительных соединений
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

"""from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings.base import Base

# SQLite configuration
DATABASE_URL = "sqlite+aiosqlite:///./project.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL запросов
    connect_args={"check_same_thread": False}  # Нужно для SQLite
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

async def create_tables():
    from models.user import User
    from models.mood import MoodCalendar
    from models.thought import ThoughtRecord
    from models.test import Test
    from models.question import Question
    from models.result import Result
    from models.feedback import Feedback
    from models.interpretation import TestInterpretation
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def recreate_tables():
    await delete_tables()
    await create_tables()"""