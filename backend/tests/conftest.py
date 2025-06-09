import pytest
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from settings.database import get_session
from settings.base import Base
from settings.config import settings
from models.user import User
from services.auth import AuthService

# Тестовая база данных PostgreSQL
TEST_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/test_psychology_db"

engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    pool_size=5,
    max_overflow=5
)

TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(autouse=True)
async def setup_db():
    # Создаем все таблицы перед тестами
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Удаляем все таблицы после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def client(session) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(session: AsyncSession):
    user_data = {
        "username": "testuser",
        "login": "test@example.com",
        "password": "testpassword123"
    }
    user = await AuthService.register_user(user_data, session)
    return user

@pytest.fixture
async def test_admin(session: AsyncSession):
    admin_data = {
        "username": "admin",
        "login": "admin@gmail.com",
        "password": "adminpass123"
    }
    admin = await AuthService.register_user(admin_data, session)
    return admin

@pytest.fixture
async def token(test_user: User, client: AsyncClient):
    response = await client.post(
        "/auth/login",
        data={
            "username": test_user.login,
            "password": "testpassword123"
        }
    )
    return response.json()["access_token"]

@pytest.fixture
async def authorized_client(client: AsyncClient, token: str):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client 

"""import pytest
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from settings.database import get_session
from settings.base import Base
from models.user import User
from services.auth import AuthService

# Используем SQLite в памяти для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def client(session) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

"""