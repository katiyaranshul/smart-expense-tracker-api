from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters

from apps.common.permissions import IsOwner
from apps.common.schema import BUDGET_REQUEST_EXAMPLE, EXPENSE_REQUEST_EXAMPLE, SUCCESS_RESPONSE_EXAMPLE
from apps.common.viewsets import StandardModelViewSet

from .filters import ExpenseFilter
from .models import Budget, Category, Expense
from .serializers import BudgetSerializer, CategorySerializer, ExpenseSerializer


@extend_schema_view(
    list=extend_schema(tags=["Categories"], summary="List categories", examples=[SUCCESS_RESPONSE_EXAMPLE]),
    retrieve=extend_schema(tags=["Categories"], summary="Retrieve category"),
    create=extend_schema(tags=["Categories"], summary="Create category", examples=[SUCCESS_RESPONSE_EXAMPLE]),
    update=extend_schema(tags=["Categories"], summary="Update category"),
    partial_update=extend_schema(tags=["Categories"], summary="Partially update category"),
    destroy=extend_schema(tags=["Categories"], summary="Delete category"),
)
class CategoryViewSet(StandardModelViewSet):
    queryset = Category.objects.none()
    serializer_class = CategorySerializer
    permission_classes = [IsOwner]
    create_message = "Category created successfully"
    retrieve_message = "Category retrieved successfully"
    list_message = "Categories retrieved successfully"
    update_message = "Category updated successfully"
    destroy_message = "Category deleted successfully"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Category.objects.none()
        return Category.objects.filter(user=self.request.user).order_by("name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        tags=["Expenses"],
        summary="List expenses",
        description="Filter by category, amount range, and date range. Search by title and order by amount or date.",
        examples=[SUCCESS_RESPONSE_EXAMPLE],
    ),
    retrieve=extend_schema(tags=["Expenses"], summary="Retrieve expense"),
    create=extend_schema(tags=["Expenses"], summary="Create expense", examples=[EXPENSE_REQUEST_EXAMPLE]),
    update=extend_schema(tags=["Expenses"], summary="Update expense"),
    partial_update=extend_schema(tags=["Expenses"], summary="Partially update expense"),
    destroy=extend_schema(tags=["Expenses"], summary="Delete expense"),
)
class ExpenseViewSet(StandardModelViewSet):
    queryset = Expense.objects.none()
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
        if getattr(self, "swagger_fake_view", False):
            return Expense.objects.none()
        return (
            Expense.objects.select_related("category")
            .filter(user=self.request.user)
            .order_by("-expense_date", "-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(tags=["Budgets"], summary="List budgets", examples=[SUCCESS_RESPONSE_EXAMPLE]),
    retrieve=extend_schema(tags=["Budgets"], summary="Retrieve budget"),
    create=extend_schema(tags=["Budgets"], summary="Create budget", examples=[BUDGET_REQUEST_EXAMPLE]),
    update=extend_schema(tags=["Budgets"], summary="Update budget"),
    partial_update=extend_schema(tags=["Budgets"], summary="Partially update budget"),
    destroy=extend_schema(tags=["Budgets"], summary="Delete budget"),
)
class BudgetViewSet(StandardModelViewSet):
    queryset = Budget.objects.none()
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
        if getattr(self, "swagger_fake_view", False):
            return Budget.objects.none()
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
