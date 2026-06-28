from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationTests(APITestCase):
    def test_user_can_register_and_login(self):
        register_payload = {
            "username": "anshul",
            "email": "anshul@example.com",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }

        register_response = self.client.post(reverse("register"), register_payload, format="json")
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(register_response.data["success"])

        login_response = self.client.post(
            reverse("login"),
            {"username": "anshul", "password": "StrongPass123!"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data["data"])

    def test_profile_requires_authentication(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_registration_rejects_duplicate_email(self):
        User.objects.create_user(username="existing", email="anshul@example.com", password="StrongPass123!")
        payload = {
            "username": "new-user",
            "email": "ANSHUL@example.com",
            "password": "StrongPass123!",
            "password_confirm": "StrongPass123!",
        }

        response = self.client.post(reverse("register"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("email", response.data["errors"])
