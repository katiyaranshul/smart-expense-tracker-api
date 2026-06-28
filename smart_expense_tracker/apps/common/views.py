from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.common.responses import success_response


class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return success_response("API is healthy", {"status": "ok"})
