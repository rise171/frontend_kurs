# Психологический сервис самомониторинга

Веб-приложение для психологического самомониторинга и оценки состояния пользователей.

## Требования

- Python 3.8+
- PostgreSQL или SQLite
- pip (менеджер пакетов Python)

## Установка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd project_kurs
```

2. Создайте виртуальное окружение:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Настройка окружения

1. Создайте файл `.env` в корневой директории проекта:
```env
# База данных
DATABASE_URL=sqlite:///./app.db  # Для SQLite
# Или для PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# Безопасность
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Настройки приложения
ADMIN_EMAIL=admin@gmail.com
```

2. Настройте базу данных:
- Для SQLite: база данных создастся автоматически
- Для PostgreSQL:
  ```bash
  # Создайте базу данных
  createdb dbname
  ```

## Запуск приложения

1. Запустите сервер разработки:
```bash
uvicorn main:app --reload
```

2. Откройте в браузере:
- API: http://localhost:8000
- Swagger документация: http://localhost:8000/docs
- ReDoc документация: http://localhost:8000/redoc

## Структура проекта

```
project_kurs/
├── api/                 # API endpoints
├── models/             # Модели базы данных
├── repository/         # Репозитории для работы с БД
├── schemas/            # Pydantic схемы
├── services/           # Бизнес-логика
├── settings/           # Конфигурация
├── tests/              # Тесты
├── .env               # Переменные окружения
├── main.py            # Точка входа
└── requirements.txt   # Зависимости
```

## API Endpoints

### Аутентификация
- POST `/auth/register` - Регистрация нового пользователя
- POST `/auth/login` - Вход в систему

### Мысли
- GET `/thoughts` - Получение списка мыслей
- POST `/thoughts` - Создание новой записи
- PUT `/thoughts/{id}` - Обновление записи
- DELETE `/thoughts/{id}` - Удаление записи

### Настроение
- GET `/mood` - Получение записей настроения
- POST `/mood` - Создание новой записи
- PUT `/mood/{id}` - Обновление записи

### Тесты
- GET `/testing/tests` - Получение списка тестов
- POST `/testing/tests` - Создание нового теста (только админ)
- GET `/testing/results` - Получение результатов

### Обратная связь
- POST `/feedback` - Отправка обратной связи
- GET `/feedback/my` - Получение своих обращений

## Роли пользователей

1. **Пользователь**
   - Создание и управление своими записями
   - Прохождение тестов
   - Отправка обратной связи

2. **Администратор**
   - Все права пользователя
   - Управление тестами
   - Ответы на обратную связь
   - Просмотр статистики

## Разработка

### Создание миграций
```bash
alembic revision --autogenerate -m "описание изменений"
alembic upgrade head
```

### Запуск тестов
```bash
pytest
```

## Дополнительная информация

### Работа с API
- Все запросы (кроме регистрации и входа) требуют токен авторизации
- Токен передается в заголовке: `Authorization: Bearer <token>`
- Формат даты: ISO 8601 (YYYY-MM-DD)

### Безопасность
- Пароли хешируются с использованием bcrypt
- Используется JWT для аутентификации
- Реализована защита от CORS

## Поддержка

При возникновении проблем:
1. Проверьте актуальность зависимостей
2. Убедитесь в правильности настроек в .env
3. Проверьте права доступа к файлам и БД

## Лицензия

MIT License