import pytest
from httpx import AsyncClient
from datetime import datetime

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def thought_data():
    return {
        "situation": "Test situation",
        "thought": "Test thought",
        "emotion": "Test emotion",
        "behavior": "Test behavior",
        "date": datetime.utcnow().isoformat()
    }

async def test_create_thought(authorized_client: AsyncClient, test_user, thought_data):
    thought_data["user_id"] = test_user.id
    response = await authorized_client.post("/thoughts/", json=thought_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["situation"] == thought_data["situation"]
    assert data["thought"] == thought_data["thought"]
    assert data["user_id"] == test_user.id

async def test_create_thought_unauthorized(client: AsyncClient, test_user, thought_data):
    thought_data["user_id"] = test_user.id
    response = await client.post("/thoughts/", json=thought_data)
    assert response.status_code == 401

async def test_create_thought_for_other_user(authorized_client: AsyncClient, test_user, thought_data):
    thought_data["user_id"] = test_user.id + 1  # Другой пользователь
    response = await authorized_client.post("/thoughts/", json=thought_data)
    assert response.status_code == 403

async def test_get_thoughts(authorized_client: AsyncClient, test_user):
    response = await authorized_client.get(f"/thoughts/?user_id={test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

async def test_get_thoughts_unauthorized(client: AsyncClient, test_user):
    response = await client.get(f"/thoughts/?user_id={test_user.id}")
    assert response.status_code == 401

async def test_get_thoughts_other_user(authorized_client: AsyncClient, test_user):
    response = await authorized_client.get(f"/thoughts/?user_id={test_user.id + 1}")
    assert response.status_code == 403

async def test_update_thought(authorized_client: AsyncClient, test_user, thought_data):
    # Создаем мысль
    thought_data["user_id"] = test_user.id
    create_response = await authorized_client.post("/thoughts/", json=thought_data)
    thought_id = create_response.json()["id"]
    
    # Обновляем мысль
    update_data = {
        "situation": "Updated situation",
        "thought": "Updated thought",
        "emotion": "Updated emotion",
        "behavior": "Updated behavior"
    }
    response = await authorized_client.put(
        f"/thoughts/{thought_id}?user_id={test_user.id}",
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["situation"] == update_data["situation"]
    assert data["thought"] == update_data["thought"]

async def test_update_nonexistent_thought(authorized_client: AsyncClient, test_user):
    update_data = {
        "situation": "Updated situation",
        "thought": "Updated thought",
        "emotion": "Updated emotion",
        "behavior": "Updated behavior"
    }
    response = await authorized_client.put(
        f"/thoughts/999?user_id={test_user.id}",
        json=update_data
    )
    assert response.status_code == 404

async def test_delete_thought(authorized_client: AsyncClient, test_user, thought_data):
    # Создаем мысль
    thought_data["user_id"] = test_user.id
    create_response = await authorized_client.post("/thoughts/", json=thought_data)
    thought_id = create_response.json()["id"]
    
    # Удаляем мысль
    response = await authorized_client.delete(
        f"/thoughts/{thought_id}?user_id={test_user.id}"
    )
    assert response.status_code == 200
    
    # Проверяем, что мысль удалена
    get_response = await authorized_client.get(
        f"/thoughts/{thought_id}?user_id={test_user.id}"
    )
    assert get_response.status_code == 404

async def test_delete_nonexistent_thought(authorized_client: AsyncClient, test_user):
    response = await authorized_client.delete(
        f"/thoughts/999?user_id={test_user.id}"
    )
    assert response.status_code == 404

# Тесты для администратора
async def test_admin_access_other_user_thoughts(
    authorized_client: AsyncClient,
    test_admin,
    test_user,
    thought_data
):
    # Создаем мысль от имени обычного пользователя
    thought_data["user_id"] = test_user.id
    create_response = await authorized_client.post("/thoughts/", json=thought_data)
    thought_id = create_response.json()["id"]
    
    # Получаем токен админа
    admin_token_response = await authorized_client.post(
        "/auth/login",
        data={
            "username": test_admin.login,
            "password": "adminpass123"
        }
    )
    admin_token = admin_token_response.json()["access_token"]
    
    # Создаем клиент с токеном админа
    admin_client = AsyncClient(
        app=authorized_client.app,
        base_url=authorized_client.base_url,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    
    # Проверяем доступ к мыслям пользователя
    response = await admin_client.get(f"/thoughts/?user_id={test_user.id}")
    assert response.status_code == 200
    
    # Проверяем возможность обновления
    update_response = await admin_client.put(
        f"/thoughts/{thought_id}?user_id={test_user.id}",
        json={
            "situation": "Admin updated",
            "thought": "Admin thought",
            "emotion": "Admin emotion",
            "behavior": "Admin behavior"
        }
    )
    assert update_response.status_code == 200 