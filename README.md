# Incident Management API

Микросервис для учета инцидентов.

## Стек технологий

- **Python 3.12** + **FastAPI**
- **PostgreSQL** + **Async SQLAlchemy**
- **Alembic** (миграции)
- **Docker** + **Docker Compose** (мультистейдж сборка)
- **Pytest** + **Httpx** (тесты)
- **Ruff** (линтер и форматтер)
- **Makefile** (автоматизация команд)

## Разработка

### Запуск локально

1.  Клонируйте репозиторий.
2.  Установите git-хуки (обязательно):
    ```bash
    make setup-hooks
    ```
3.  Запустите проект в режиме разработки:
    ```bash
    make dev-start
    ```
    Сервер будет доступен по адресу: `http://localhost:8000`
    Swagger UI: `http://localhost:8000/docs`

### Команды Makefile

*   `make dev-start` - Запуск в dev-режиме (с hot-reload).
*   `make dev-stop` - Остановка dev-окружения.
*   `make start` - Запуск в prod-режиме (оптимизированный образ).
*   `make stop` - Остановка prod-окружения.
*   `make test` - Запуск тестов.
*   `make lint` - Проверка кода линтером Ruff.
*   `make format` - Форматирование кода Ruff.
*   `make makemigration m="message"` - Создание новой миграции.

## Структура проекта

```text
.
├── app/
│   ├── api/            # Роутеры API
│   ├── core/           # Конфиги и БД
│   ├── models/         # ORM модели
│   ├── schemas/        # Pydantic схемы
│   └── main.py         # Точка входа
├── alembic/            # Миграции БД
├── tests/              # Тесты
├── docker-compose.yml  # Dev окружение
├── docker-compose.prod.yml # Prod окружение
└── Makefile            # Утилиты
```

## CI/CD

Проект настроен на запуск проверок в GitHub Actions:
1.  Установка зависимостей.
2.  Линтинг (Ruff).
3.  Тесты (Pytest).

Локальные git-хуки (`pre-commit`, `pre-push`) дублируют эти проверки, чтобы не пушить сломанный код.
