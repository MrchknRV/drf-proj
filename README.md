# Образовательная платформа «SkillForge»
### SkillForge — это современная веб-платформа для онлайн-обучения, которая помогает студентам и преподавателям эффективно взаимодействовать в процессе обучения.
### Проект разработан как бэкенд для SPA-приложения и полностью соответствует требованиям по Django REST Framework.

## Основной функционал

* Регистрация и авторизация пользователей (студенты, преподаватели, администраторы)
* JWT-авторизация (djangorestframework-simplejwt)
* Управление профилями пользователей (аватар, телефон, страна, Telegram)
* Создание, редактирование и удаление курсов (только преподавателем)
* Добавление уроков и материалов к курсу
* Прогресс прохождения курсов студентами
* Система отзывов и оценок к курсам
* Публичный список курсов и детальная информация
* Админ-панель с расширенными правами
* Асинхронные уведомления (например, о новом уроке) — через Celery + Telegram (или email)
* Пагинация, фильтрация и поиск
* Полная документация API (Swagger + ReDoc)
* Настройка CORS для фронтенда
* Покрытие тестами >80%
* Полная контейнеризация (Docker + Docker Compose)

## Технологии

- Python 3.12
- Django 5 + Django REST Framework
- JWT-авторизация
- PostgreSQL (основная БД)
- Redis + Celery (асинхронные задачи и уведомления)
- Telegram API (уведомления через requests)
- Poetry (управление зависимостями)
- drf-yasg (документация API)
- django-cors-headers (CORS)
- Gunicorn + Nginx (продакшен)
- Docker + Docker Compose (контейнеризация)
- GitHub Actions (CI/CD с тестами, линтингом и деплоем)

Локальный запуск
1. Клонируй репозиторий
```
git clone https://github.com/MrchknRV/drf-proj
cd skillforge
```

2. Установи зависимости (Poetry)
```
poetry install
```
3. Создай и заполни .env
```
cp .env.example .env
```
Открой .env и заполни:
env
```# Django
SECRET_KEY=твой_сильный_ключ
DEBUG=True

# База данных (PostgreSQL)
DATABASE_NAME=skillforge_db
DATABASE_USER=skillforge_user
DATABASE_PASSWORD=supersecretpassword
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Redis & Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Telegram (уведомления)
TELEGRAM_BOT_TOKEN=твой_токен_бота
```
4. Запусти сервисы

* Redis (если локально):
`redis-server`
* Celery worker (отдельный терминал):
```
poetry run celery -A config worker -l info
```
* Celery beat (планировщик):
```
poetry run celery -A config beat -l info
```
* Миграции и сервер:
```
poetry run python manage.py migrate
poetry run python manage.py runserver
```

5. Проверь

- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/
- Админка: http://127.0.0.1:8000/admin/

Создай суперпользователя:
```
poetry run python manage.py createsuperuser
```
Тесты
```
poetry run python manage.py test
```
Покрытие >80%: регистрация, авторизация, курсы, уроки, права доступа, пагинация.

## Документация API

* Swagger UI: http://127.0.0.1:8000/swagger/
* ReDoc: http://127.0.0.1:8000/redoc/

### Автор
Родион Марочкин — 2025 \
Проект выполнен в рамках курсовой работы по Django REST Framework.\
Готов к дальнейшему развитию (фронтенд, оплата курсов, статистика, мобильное приложение).\
Спасибо за внимание!
