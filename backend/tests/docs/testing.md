# Тестирование проекта

## Структура тестов

```
tests/
├── conftest.py              # Общие фикстуры и конфигурация
├── test_api/               # Тесты API endpoints
│   ├── test_auth.py        # Тесты аутентификации
│   ├── test_thoughts.py    # Тесты endpoint'ов мыслей
│   ├── test_mood.py        # Тесты endpoint'ов настроения
│   └── test_feedback.py    # Тесты обратной связи
├── test_services/          # Тесты сервисного слоя
├── test_repository/        # Тесты репозиториев
└── test_models/           # Тесты моделей
```

## Используемые инструменты

- **pytest**: основной фреймворк для тестирования
- **pytest-asyncio**: для тестирования асинхронного кода
- **httpx**: для тестирования HTTP endpoints
- **SQLAlchemy**: для работы с тестовой базой данных

## Запуск тестов

### Запуск всех тестов
```bash
pytest
```

### Запуск конкретного модуля
```bash
pytest tests/test_api/test_auth.py
```

### Запуск с подробным выводом
```bash
pytest -v
```

### Запуск с покрытием кода
```bash
pytest --cov=app tests/
```

## Правила написания тестов

1. **Изоляция тестов**
   - Каждый тест должен быть независимым
   - Использовать фикстуры для подготовки данных
   - Очищать тестовые данные после каждого теста

2. **Наименование тестов**
   - Начинать с `test_`
   - Описательные имена, отражающие суть теста
   - Группировать связанные тесты в классы

3. **Структура теста**
   - Arrange (подготовка данных)
   - Act (выполнение действия)
   - Assert (проверка результата)

4. **Проверка граничных случаев**
   - Позитивные сценарии
   - Негативные сценарии
   - Граничные значения
   - Обработка ошибок

## Мокирование

```python
@pytest.fixture
def mock_repository(mocker):
    """Мок репозитория"""
    return mocker.patch("repository.thought.ThoughtRepository")

async def test_service_with_mock(mock_repository):
    """Тест сервиса с моком репозитория"""
    mock_repository.get_by_id.return_value = ThoughtRecord(
        id=1,
        user_id=1,
        situation="Test"
    )
    
    result = await ThoughtService.get_thought(1, 1, AsyncSession())
    
    mock_repository.get_by_id.assert_called_once_with(1)
    assert result.id == 1
```

## Тестирование безопасности

1. **Аутентификация**
   - Проверка валидных токенов
   - Проверка невалидных токенов
   - Проверка истекших токенов

2. **Авторизация**
   - Проверка прав доступа
   - Проверка ролей пользователей
   - Проверка ограничений доступа

## Интеграционное тестирование

```python
async def test_complete_workflow(client, test_user):
    """Тест полного рабочего процесса"""
    # Логин
    login_response = await client.post(
        "/auth/login",
        data={"username": "test@test.com", "password": "testpass123"}
    )
    token = login_response.json()["access_token"]
    
    # Создание записи
    headers = {"Authorization": f"Bearer {token}"}
    create_response = await client.post(
        "/thoughts",
        json={
            "situation": "Test situation",
            "thought": "Test thought",
            "emotion": "Test emotion",
            "behavior": "Test behavior",
            "user_id": test_user.id
        },
        headers=headers
    )
    thought_id = create_response.json()["id"]
    
    # Получение записи
    get_response = await client.get(
        f"/thoughts/{thought_id}",
        headers=headers
    )
    assert get_response.status_code == 200
```

## Советы по тестированию

1. **Производительность**
   - Использовать параметризацию тестов
   - Группировать похожие тесты
   - Избегать излишних обращений к БД

2. **Поддержка тестов**
   - Регулярно обновлять тесты
   - Документировать сложные тестовые случаи
   - Следить за покрытием кода

3. **Отладка тестов**
   - Использовать pytest -s для вывода print
   - Использовать отладчик
   - Логировать важные операции 