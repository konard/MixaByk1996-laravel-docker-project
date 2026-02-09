# Avito Bot & Email Campaign System

Автоматизированный бот для управления объявлениями на Avito и email-рассылок.

## Технологический стек

- **Backend**: Python 3.11 + FastAPI
- **Frontend**: Vue.js 3 + Vite
- **База данных**: PostgreSQL 15
- **Кеш/Очереди**: Redis 7 + Celery
- **Контейнеризация**: Docker + Docker Compose
- **Веб-сервер**: Nginx (reverse proxy)

## Быстрый старт

```bash
# Клонировать репозиторий
git clone <repo-url>
cd laravel-docker-project

# Скопировать конфигурацию
cp .env.example .env

# Запустить все сервисы
docker-compose up -d --build

# Применить миграции БД
docker-compose exec backend alembic upgrade head
```

Приложение будет доступно:
- **Frontend**: http://localhost
- **API**: http://localhost/api/v1
- **API Docs (Swagger)**: http://localhost/api/docs

## Структура проекта

```
├── backend/              # FastAPI приложение
│   ├── app/
│   │   ├── api/v1/       # API эндпоинты
│   │   ├── core/         # Конфигурация, безопасность
│   │   ├── models/       # SQLAlchemy модели
│   │   ├── schemas/      # Pydantic схемы
│   │   ├── services/     # Бизнес-логика
│   │   └── tasks/        # Celery задачи
│   ├── alembic/          # Миграции БД
│   └── tests/            # Юнит-тесты
├── frontend/             # Vue.js приложение
│   └── src/
│       ├── components/   # UI компоненты
│       ├── views/        # Страницы
│       ├── router/       # Маршрутизация
│       └── store/        # Pinia хранилище
├── nginx/                # Конфигурация Nginx
└── docker-compose.yml
```

## Основные функции

### Avito (через официальное API)
- Публикация и управление объявлениями
- Сбор аналитики (просмотры, избранное, контакты)
- Мониторинг конкурентов
- Автоответы на сообщения

### Email-рассылки
- Импорт контактов из CSV/Excel
- Визуальный редактор шаблонов
- Персонализация и сегментация
- A/B-тестирование
- Аналитика (открытия, клики, отписки)

### CRM
- База контактов с историей взаимодействий
- Сегменты по интересам, географии
- Импорт/экспорт CSV/Excel

## API Документация

После запуска доступна по адресу http://localhost/api/docs (Swagger UI).

## Тестирование

```bash
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=app
```
