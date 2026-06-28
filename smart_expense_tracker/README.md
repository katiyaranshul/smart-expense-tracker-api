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

## How It Works

Users first register and log in through the authentication endpoints. After login, the API returns access and refresh tokens. The access token is sent with protected requests using the `Authorization: Bearer <token>` header.

Once authenticated, a user can create categories such as Food, Travel, Shopping, Bills, or Health. Expenses are then added under those categories with an amount and expense date.

Budgets are created per month and year. The analytics endpoints compare monthly spending against the user's budget and return useful summaries such as total spent, remaining budget, percentage used, top expenses, and category-wise spending.

## Core API Modules

### Authentication

Handles user registration, login, token refresh, and profile retrieval.

```text
POST /api/v1/auth/register/
POST /api/v1/auth/login/
POST /api/v1/auth/token/refresh/
GET  /api/v1/auth/profile/
```

### Categories

Allows users to create and manage their own expense categories. Category names are unique per user.

```text
/api/v1/categories/
```

### Expenses

Allows users to create, view, update, delete, filter, search, and order their own expenses.

```text
/api/v1/expenses/
```

Supported expense filters include:

```text
category
min_amount
max_amount
start_date
end_date
search
ordering
```

### Budgets

Allows users to set one budget per month and year.

```text
/api/v1/budgets/
```

### Analytics

Provides read-only spending insights for the authenticated user.

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

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- django-filter
- drf-spectacular
- Docker
