# Smart Expense Tracker & Analytics API

Production-style Django REST Framework backend for personal expense tracking, budgets, categories, and spending analytics.

The application code lives in [`smart_expense_tracker/`](smart_expense_tracker/). See that directory's [README](smart_expense_tracker/README.md) for installation, environment variables, Docker commands, migrations, tests, and API examples.

## Quick start

```bash
cd smart_expense_tracker
cp .env.example .env
docker compose up --build
```

Then open:

- API docs: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- Health check: [http://127.0.0.1:8000/api/health/](http://127.0.0.1:8000/api/health/)

## Highlights

- JWT authentication with registration, login, and profile endpoints
- User-scoped categories, expenses, and monthly budgets
- Filtering, search, ordering, and pagination on expenses
- Analytics endpoints for monthly totals, category breakdowns, top expenses, and budget status
- Standardized success and error responses
- OpenAPI/Swagger documentation via drf-spectacular
- Docker Compose setup with PostgreSQL and API health checks
