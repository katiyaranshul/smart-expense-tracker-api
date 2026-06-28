from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Expense


User = get_user_model()


class ExpenseAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="StrongPass123!")
        self.other_user = User.objects.create_user(username="other", password="StrongPass123!")
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(user=self.user, name="Food")
        self.other_category = Category.objects.create(user=self.other_user, name="Travel")

    def test_user_can_create_expense_for_own_category(self):
        payload = {
            "title": "Lunch",
            "amount": "250.00",
            "expense_date": "2026-06-20",
            "category": self.category.id,
        }

        response = self.client.post(reverse("expense-list"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(Expense.objects.filter(user=self.user).count(), 1)

    def test_user_cannot_use_another_users_category(self):
        payload = {
            "title": "Flight",
            "amount": "2500.00",
            "expense_date": "2026-06-20",
            "category": self.other_category.id,
        }

        response = self.client.post(reverse("expense-list"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    def test_expense_filtering_by_amount(self):
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Coffee",
            amount=Decimal("80.00"),
            expense_date="2026-06-01",
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Dinner",
            amount=Decimal("1200.00"),
            expense_date="2026-06-02",
        )

        response = self.client.get(reverse("expense-list"), {"min_amount": "100"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["count"], 1)
        self.assertEqual(response.data["data"]["results"][0]["title"], "Dinner")


class CategoryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="StrongPass123!")
        self.client.force_authenticate(self.user)

    def test_category_name_is_unique_per_user(self):
        Category.objects.create(user=self.user, name="Food")

        response = self.client.post(reverse("category-list"), {"name": "food"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
