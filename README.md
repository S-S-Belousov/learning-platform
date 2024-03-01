# Learning Platform

Learning Platform - это веб-приложение для обучения онлайн, которое позволяет пользователям создавать, просматривать и управлять уроками, продуктами и группами студентов.

## Настройка проекта

1. Клонируйте репозиторий:

```bash
git clone https://github.com/S-S-Belousov/learning-platform.git
```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Выполните миграции:
```bash
python manage.py migrate
```
4. Запустите сервер:
```bash
python manage.py runserver
```
## Использование проекта
После запуска сервера перейдите по адресу http://localhost:8000/admin/ для доступа к панели администратора.
Чтобы использовать API, перейдите по адресу http://localhost:8000/api/.
Для аутентификации через API используйте эндпоинт http://localhost:8000/api/login/.
Для выхода из учетной записи используйте эндпоинт http://localhost:8000/api/logout/.

## Описание API проекта

# Продукты (Products)
**GET /api/products/**
Возвращает список всех продуктов на платформе.

**POST /api/products/**
Создает новый продукт.

**GET /api/products/{product_id}/**
Возвращает информацию о конкретном продукте.

**PUT /api/products/{product_id}/**
Обновляет информацию о конкретном продукте.

**DELETE /api/products/{product_id}/**
Удаляет конкретный продукт.

# Уроки (Lessons)
**GET /api/lessons/**
Возвращает список всех уроков.

**POST /api/lessons/**
Создает новый урок.

**GET /api/lessons/{lesson_id}/**
Возвращает информацию о конкретном уроке.

**PUT /api/lessons/{lesson_id}/**
Обновляет информацию о конкретном уроке.

**DELETE /api/lessons/{lesson_id}/**
Удаляет конкретный урок.

# Группы (Groups)
**GET /api/groups/**
Возвращает список всех групп.

**POST /api/groups/**
Создает новую группу.

**GET /api/groups/{group_id}/**
Возвращает информацию о конкретной группе.

**PUT /api/groups/{group_id}/**
Обновляет информацию о конкретной группе.

**DELETE /api/groups/{group_id}/**
Удаляет конкретную группу.

# Аутентификация
**POST /api/login/**
Аутентифицирует пользователя и возвращает токен доступа.

**POST /api/logout/**
Выходит из учетной записи пользователя.