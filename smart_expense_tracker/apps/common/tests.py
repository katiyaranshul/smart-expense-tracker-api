from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTests(APITestCase):
    def test_health_check_is_public(self):
        for url_name in ("health-check", "health-check-api"):
            response = self.client.get(reverse(url_name))

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response.data["success"])
            self.assertEqual(response.data["data"]["status"], "ok")
