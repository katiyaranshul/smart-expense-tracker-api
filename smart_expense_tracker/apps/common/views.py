from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.responses import success_response
from apps.common.schema import SUCCESS_RESPONSE_EXAMPLE


@extend_schema(
    tags=["Health"],
    summary="Health check",
    description="Public endpoint for load balancers and deployment health checks.",
    responses={
        200: OpenApiResponse(
            description="Healthy API",
            response={"type": "object", "properties": {"success": {"type": "boolean"}, "message": {"type": "string"}, "data": {"type": "object"}}},
            examples=[
                OpenApiExample(
                    "Healthy API",
                    value={"success": True, "message": "API is healthy", "data": {"status": "ok"}},
                    response_only=True,
                )
            ],
        )
    },
)
class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return success_response("API is healthy", {"status": "ok"})
