from rest_framework import serializers

from apps.expenses.models import Expense


class AnalyticsQuerySerializer(serializers.Serializer):
    month = serializers.IntegerField(min_value=1, max_value=12, required=False)
    year = serializers.IntegerField(min_value=2000, max_value=2100, required=False)


class MonthlySummarySerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    total_expense = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()


class CategorySummaryItemSerializer(serializers.Serializer):
    category = serializers.CharField()
    total = serializers.DecimalField(max_digits=12, decimal_places=2)


class BudgetStatusSerializer(serializers.Serializer):
    month = serializers.CharField()
    year = serializers.IntegerField()
    budget_limit = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    percentage_used = serializers.DecimalField(max_digits=6, decimal_places=2, allow_null=True)


class AnalyticsExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = ("id", "title", "amount", "expense_date", "category", "category_name")
