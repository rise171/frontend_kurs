import pytest
from httpx import AsyncClient
from main import app
from models.user import UserRole

pytestmark = pytest.mark.asyncio

async def test_register_user(client):
    response = await client.post(
        "/user/register",
        json={
            "username": "newuser",
            "login": "new@example.com",
            "password": "newpassword",
            "role": UserRole.USER
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["login"] == "new@example.com"
    assert data["role"] == UserRole.USER

async def test_register_admin(client):
    response = await client.post(
        "/user/register",
        json={
            "username": "newadmin",
            "login": "admin@gmail.com",
            "password": "adminpass",
            "role": UserRole.USER  # Даже если указана роль USER
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newadmin"
    assert data["login"] == "admin@gmail.com"
    assert data["role"] == UserRole.ADMIN  # Должна быть установлена роль ADMIN

async def test_login_user(client, test_user):
    response = await client.post(
        "/user/login",
        json={
            "login": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_credentials(client):
    response = await client.post(
        "/user/login",
        json={
            "login": "wrong@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401 