from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.expenses.models import Budget, Category, Expense


User = get_user_model()


class AnalyticsAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="StrongPass123!")
        self.client.force_authenticate(self.user)
        self.category = Category.objects.create(user=self.user, name="Food")
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Groceries",
            amount=Decimal("1200.00"),
            expense_date="2026-06-10",
        )
        Expense.objects.create(
            user=self.user,
            category=self.category,
            title="Lunch",
            amount=Decimal("250.00"),
            expense_date="2026-06-11",
        )
        Budget.objects.create(user=self.user, month=6, year=2026, limit_amount=Decimal("2000.00"))

    def test_monthly_analytics(self):
        response = self.client.get(reverse("analytics-monthly"), {"month": 6, "year": 2026})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["transaction_count"], 2)
        self.assertEqual(response.data["data"]["total_expense"], Decimal("1450.00"))

    def test_budget_status(self):
        response = self.client.get(reverse("analytics-budget-status"), {"month": 6, "year": 2026})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["remaining_amount"], Decimal("550.00"))
        self.assertEqual(response.data["data"]["percentage_used"], Decimal("72.50"))
