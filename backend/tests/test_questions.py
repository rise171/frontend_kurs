import pytest
from unittest.mock import Mock, patch
from services.question import QuestionService
from schemas.question import QuestionCreate, QuestionGetting
from models.question import Question
from fastapi import HTTPException

pytestmark = pytest.mark.asyncio

@pytest.fixture
def mock_question():
    return Question(
        id=1,
        test_id=1,
        sentence="Test question?",
        options=["Option 1", "Option 2", "Option 3"],
        correct_option=1,
        score=10
    )

async def test_get_question(client, test_user, mock_question):
    # Мокаем сервис
    with patch('services.question.QuestionService.get_question') as mock_get:
        mock_get.return_value = QuestionGetting.model_validate(mock_question)
        
        # Получаем токен для авторизации
        login_response = await client.post(
            "/user/login",
            json={
                "login": "test@example.com",
                "password": "testpassword"
            }
        )
        token = login_response.json()["access_token"]
        
        # Делаем запрос с токеном
        response = await client.get(
            "/questions/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["sentence"] == "Test question?"
        assert len(data["options"]) == 3
        assert data["score"] == 10

async def test_get_test_questions(client, test_user, mock_question):
    # Мокаем сервис
    with patch('services.question.QuestionService.get_test_questions') as mock_get:
        mock_get.return_value = [QuestionGetting.model_validate(mock_question)]
        
        # Получаем токен для авторизации
        login_response = await client.post(
            "/user/login",
            json={
                "login": "test@example.com",
                "password": "testpassword"
            }
        )
        token = login_response.json()["access_token"]
        
        # Делаем запрос с токеном
        response = await client.get(
            "/questions/test/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["test_id"] == 1
        assert data[0]["sentence"] == "Test question?"

async def test_get_test_question(client, test_user, mock_question):
    # Мокаем сервис
    with patch('services.question.QuestionService.get_test_question') as mock_get:
        mock_get.return_value = QuestionGetting.model_validate(mock_question)
        
        # Получаем токен для авторизации
        login_response = await client.post(
            "/user/login",
            json={
                "login": "test@example.com",
                "password": "testpassword"
            }
        )
        token = login_response.json()["access_token"]
        
        # Делаем запрос с токеном
        response = await client.get(
            "/questions/test/1/question/1",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["test_id"] == 1
        assert data["sentence"] == "Test question?"
        assert len(data["options"]) == 3
        assert data["score"] == 10

async def test_get_question_unauthorized(client):
    response = await client.get("/questions/1")
    assert response.status_code == 401

async def test_get_question_not_found(client, test_user):
    # Мокаем сервис, чтобы он возвращал None
    with patch('services.question.QuestionService.get_question') as mock_get:
        mock_get.return_value = None
        
        # Получаем токен для авторизации
        login_response = await client.post(
            "/user/login",
            json={
                "login": "test@example.com",
                "password": "testpassword"
            }
        )
        token = login_response.json()["access_token"]
        
        # Делаем запрос с токеном
        response = await client.get(
            "/questions/999",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Question not found"

async def test_get_test_question_not_found(client, test_user):
    # Мокаем сервис, чтобы он возвращал None
    with patch('services.question.QuestionService.get_test_question') as mock_get:
        mock_get.side_effect = HTTPException(status_code=404, detail="Question not found in this test")
        
        # Получаем токен для авторизации
        login_response = await client.post(
            "/user/login",
            json={
                "login": "test@example.com",
                "password": "testpassword"
            }
        )
        token = login_response.json()["access_token"]
        
        # Делаем запрос с токеном
        response = await client.get(
            "/questions/test/1/question/999",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 404
        assert response.json()["detail"] == "Question not found in this test" 