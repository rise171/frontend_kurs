import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio

async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "login": "new@example.com",
            "password": "newpassword123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["login"] == "new@example.com"
    assert "id" in data

async def test_register_duplicate_login(client: AsyncClient, test_user):
    response = await client.post(
        "/auth/register",
        json={
            "username": "another",
            "login": test_user.login,  # Используем существующий email
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

async def test_login_success(client: AsyncClient, test_user):
    response = await client.post(
        "/auth/login",
        data={
            "username": test_user.login,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_wrong_password(client: AsyncClient, test_user):
    response = await client.post(
        "/auth/login",
        data={
            "username": test_user.login,
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "incorrect login or password" in response.json()["detail"].lower()

async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 401
    assert "incorrect login or password" in response.json()["detail"].lower()

async def test_get_current_user(authorized_client: AsyncClient, test_user):
    response = await authorized_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username
    assert data["login"] == test_user.login

async def test_get_current_user_no_token(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 401
    assert "not authenticated" in response.json()["detail"].lower()

async def test_register_admin(client: AsyncClient):
    response = await client.post(
        "/auth/register",
        json={
            "username": "admin",
            "login": "admin@gmail.com",  # Специальный email для админа
            "password": "adminpass123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["role"] == "admin" 