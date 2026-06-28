import logging
import time


logger = logging.getLogger("request")


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start_time) * 1000

        user = getattr(request, "user", None)
        username = user.get_username() if user and user.is_authenticated else "anonymous"
        logger.info(
            "method=%s endpoint=%s status=%s duration_ms=%.2f user=%s",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
            username,
        )
        return response
