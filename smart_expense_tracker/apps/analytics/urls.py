from django.urls import path

from .views import (
    BudgetStatusAPIView,
    CategoryAnalyticsAPIView,
    MonthlyAnalyticsAPIView,
    TopExpensesAPIView,
)


urlpatterns = [
    path("monthly/", MonthlyAnalyticsAPIView.as_view(), name="analytics-monthly"),
    path("category/", CategoryAnalyticsAPIView.as_view(), name="analytics-category"),
    path("top-expenses/", TopExpensesAPIView.as_view(), name="analytics-top-expenses"),
    path("budget-status/", BudgetStatusAPIView.as_view(), name="analytics-budget-status"),
]
