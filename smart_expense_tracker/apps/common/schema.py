from drf_spectacular.utils import OpenApiExample


SUCCESS_RESPONSE_EXAMPLE = OpenApiExample(
    "Success response",
    value={
        "success": True,
        "message": "Request completed successfully",
        "data": {},
    },
    response_only=True,
)

ERROR_RESPONSE_EXAMPLE = OpenApiExample(
    "Validation error",
    value={
        "success": False,
        "message": "Validation failed",
        "errors": {"field_name": ["This field is required."]},
    },
    response_only=True,
)

REGISTER_REQUEST_EXAMPLE = OpenApiExample(
    "Register request",
    value={
        "username": "anshul",
        "email": "anshul@example.com",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    },
    request_only=True,
)

LOGIN_REQUEST_EXAMPLE = OpenApiExample(
    "Login request",
    value={"username": "anshul", "password": "StrongPass123!"},
    request_only=True,
)

LOGIN_RESPONSE_EXAMPLE = OpenApiExample(
    "Login response",
    value={
        "success": True,
        "message": "Login successful",
        "data": {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        },
    },
    response_only=True,
)

EXPENSE_REQUEST_EXAMPLE = OpenApiExample(
    "Create expense request",
    value={
        "title": "Lunch",
        "amount": "250.00",
        "expense_date": "2026-06-20",
        "category": 1,
        "description": "Team lunch",
    },
    request_only=True,
)

BUDGET_REQUEST_EXAMPLE = OpenApiExample(
    "Create budget request",
    value={"month": 6, "year": 2026, "limit_amount": "2000.00"},
    request_only=True,
)

AUTH_HEADER_EXAMPLE = OpenApiExample(
    "Authenticated request header",
    value="Authorization: Bearer <access_token>",
    parameter_only=("Authorization", "header"),
)
