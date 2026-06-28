from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from apps.common.permissions import IsOwner
from apps.common.viewsets import StandardModelViewSet

from .filters import ExpenseFilter
from .models import Budget, Category, Expense
from .serializers import BudgetSerializer, CategorySerializer, ExpenseSerializer


class CategoryViewSet(StandardModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]
    create_message = "Category created successfully"
    retrieve_message = "Category retrieved successfully"
    list_message = "Categories retrieved successfully"
    update_message = "Category updated successfully"
    destroy_message = "Category deleted successfully"

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(StandardModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ExpenseFilter
    search_fields = ["title"]
    ordering_fields = ["amount", "expense_date"]
    ordering = ["-expense_date"]
    create_message = "Expense created successfully"
    retrieve_message = "Expense retrieved successfully"
    list_message = "Expenses retrieved successfully"
    update_message = "Expense updated successfully"
    destroy_message = "Expense deleted successfully"

    def get_queryset(self):
        return Expense.objects.select_related("category").filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetViewSet(StandardModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [IsOwner]
    ordering_fields = ["month", "year", "limit_amount"]
    ordering = ["-year", "-month"]
    create_message = "Budget created successfully"
    retrieve_message = "Budget retrieved successfully"
    list_message = "Budgets retrieved successfully"
    update_message = "Budget updated successfully"
    destroy_message = "Budget deleted successfully"

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
