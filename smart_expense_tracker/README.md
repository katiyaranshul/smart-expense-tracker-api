# Smart Expense Tracker & Analytics API

Smart Expense Tracker & Analytics API is a backend system for managing personal expenses, budgets, categories, and spending insights. It is built with Django, Django REST Framework, PostgreSQL, JWT authentication, and Docker.

## About The Project

This project provides a secure REST API where each user can create an account, log in, organize expenses by category, set monthly budgets, and view analytics about their spending behavior.

The API is designed so every user's data is private. Categories, expenses, and budgets are always scoped to the authenticated user, meaning users can only view or modify their own records.

## Main Features

- User registration and JWT-based login
- Authenticated user profile endpoint
- Category management for organizing expenses
- Expense tracking with amount, date, category, title, and description
- Monthly budget management
- Expense filtering by category, amount range, and date range
- Search expenses by title
- Sort expenses by amount or date
- Paginated API responses
- Spending analytics using Django ORM aggregations
- Standard success and error response format
- Request logging middleware
- Swagger/OpenAPI documentation
- Public health check endpoint for deployments

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- django-filter
- drf-spectacular
- Docker

## Installation

### Local development (Python)

```bash
cd smart_expense_tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Environment variables

Configure these values in `.env`:

| Variable | Description | Default |
| --- | --- | --- |
| `SECRET_KEY` | Django secret key | development fallback |
| `DEBUG` | Enable debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated hostnames | `localhost,127.0.0.1` |
| `TIME_ZONE` | Application timezone | `UTC` |
| `POSTGRES_DB` | Database name | `smart_expense_tracker` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `ACCESS_TOKEN_MINUTES` | JWT access token lifetime | `30` |
| `REFRESH_TOKEN_DAYS` | JWT refresh token lifetime | `7` |
| `REQUEST_LOG_LEVEL` | Request logger level | `INFO` |
| `USE_SQLITE` | Use SQLite instead of PostgreSQL | `False` |

For quick local testing without PostgreSQL, set `USE_SQLITE=True` in `.env`.

## Running migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Running the server

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`.

## Docker

Build and start the API with PostgreSQL:

```bash
docker compose up --build
```

Useful commands:

```bash
docker compose build
docker compose up -d
docker compose logs -f api
docker compose down
```

The API container runs migrations on startup and exposes port `8000`.

## Running tests

```bash
USE_SQLITE=True python manage.py test
```

## API documentation

- OpenAPI schema: `GET /api/schema/`
- Swagger UI: `GET /api/docs/`
- Health check: `GET /api/health/`

## Authentication

Register a user, then log in to receive JWT tokens. Send the access token with protected requests:

```http
Authorization: Bearer <access_token>
```

### Register

```http
POST /api/v1/auth/register/
Content-Type: application/json

{
  "username": "anshul",
  "email": "anshul@example.com",
  "password": "StrongPass123!",
  "password_confirm": "StrongPass123!"
}
```

Example response:

```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "anshul",
    "email": "anshul@example.com",
    "first_name": "",
    "last_name": "",
    "date_joined": "2026-06-25T12:00:00Z"
  }
}
```

### Login

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "anshul",
  "password": "StrongPass123!"
}
```

Example response:

```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "refresh": "eyJ...",
    "access": "eyJ..."
  }
}
```

## Core API Modules

### Authentication

```text
POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/token/refresh/
GET  /api/v1/auth/profile/
```

### Categories

```text
/api/v1/categories/
```

### Expenses

```text
/api/v1/expenses/
```

Supported expense filters:

```text
category
min_amount
max_amount
start_date
end_date
search
ordering
```

Example create expense request:

```json
{
  "title": "Lunch",
  "amount": "250.00",
  "expense_date": "2026-06-20",
  "category": 1,
  "description": "Team lunch"
}
```

### Budgets

```text
/api/v1/budgets/
```

### Analytics

```text
GET /api/v1/analytics/monthly/
GET /api/v1/analytics/category/
GET /api/v1/analytics/top-expenses/
GET /api/v1/analytics/budget-status/
```

Analytics endpoints support optional `month` and `year` query parameters.

## Response Format

Successful API responses follow this structure:

```json
{
  "success": true,
  "message": "Expense created successfully",
  "data": {}
}
```

Error responses follow this structure:

```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {}
}
```
