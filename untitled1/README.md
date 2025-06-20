# Психологический сервис

Веб-приложение для психологического тестирования и самоанализа с поддержкой PWA (Progressive Web Application).

## Функциональность

- Система авторизации и регистрации пользователей
- Психологические тесты с автоматической обработкой результатов
- Календарь настроения
- Дневник мыслей
- Обратная связь с администратором
- Административная панель для управления контентом
- Поддержка PWA для установки на устройства
- Работа в оффлайн режиме

## Технологии

- React 18
- React Router 6
- Axios для HTTP-запросов
- Service Workers для PWA
- Docker для контейнеризации
- Nginx для раздачи статики

## Требования

- Node.js 16+ (для разработки)
- Docker и Docker Compose (для развертывания)
- или Node.js 16+ (для запуска без Docker)

## Установка и запуск

### Разработка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd <папка-проекта>
```

2. Установите зависимости:
```bash
npm install
```

3. Запустите приложение в режиме разработки:
```bash
npm start
```

Приложение будет доступно по адресу http://localhost:3000

### Запуск через Docker

1. Соберите и запустите контейнеры:
```bash
docker-compose up -d --build
```

Приложение будет доступно по адресу http://localhost

### Сборка для продакшена

1. Создайте продакшен сборку:
```bash
npm run build
```

2. Соберите Docker образ:
```bash
docker build -t psychology-service .
```

3. Запустите контейнер:
```bash
docker run -d -p 80:80 psychology-service
```

## PWA функциональность

Приложение поддерживает установку на устройства как PWA:

- На Android: через баннер "Установить приложение"
- На iOS: через меню "Поделиться" -> "На экран «Домой»"
- На десктопе: через кнопку установки в адресной строке браузера

Поддерживаемые функции PWA:
- Оффлайн работа
- Кэширование данных
- Push-уведомления
- Быстрый доступ через ярлыки

## Структура проекта

```
├── public/                 # Публичные файлы
│   ├── manifest.json      # Манифест PWA
│   └── service-worker.js  # Service Worker для PWA
├── src/                   # Исходный код
│   ├── components/        # React компоненты
│   ├── context/          # Контекст приложения
│   ├── pages/            # Страницы приложения
│   └── tests/            # Тесты
├── Dockerfile            # Конфигурация Docker
├── docker-compose.yml    # Конфигурация Docker Compose
├── nginx.conf           # Конфигурация Nginx
└── package.json         # Зависимости и скрипты
```

## Тестирование

Запуск тестов:
```bash
npm test
```

Запуск тестов с покрытием:
```bash
npm run test:coverage
```

## CI/CD

Проект настроен для автоматической сборки и развертывания:

1. Сборка и тестирование при каждом push
2. Автоматическая сборка Docker образа
3. Развертывание на сервере при релизе

## Безопасность

- Все API-запросы защищены токенами
- Настроены заголовки безопасности в Nginx
- Реализована валидация форм
- Защита от XSS и CSRF атак

## Лицензия

MIT 