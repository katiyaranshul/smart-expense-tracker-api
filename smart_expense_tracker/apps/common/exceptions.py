from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(exc, exceptions.ValidationError):
        message = "Validation failed"
        errors = response.data
    elif isinstance(exc, exceptions.NotAuthenticated):
        message = "Authentication credentials were not provided"
        errors = response.data
    elif isinstance(exc, exceptions.AuthenticationFailed):
        message = "Authentication failed"
        errors = response.data
    elif isinstance(exc, exceptions.PermissionDenied):
        message = "Permission denied"
        errors = response.data
    elif isinstance(exc, Http404):
        message = "Resource not found"
        errors = response.data
    else:
        message = response.data.get("detail", "Request failed") if isinstance(response.data, dict) else "Request failed"
        errors = response.data

    response.data = {
        "success": False,
        "message": message,
        "errors": errors,
    }
    response.status_code = response.status_code or status.HTTP_400_BAD_REQUEST
    return response
