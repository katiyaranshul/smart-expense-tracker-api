from rest_framework import serializers

from apps.expenses.models import Expense


class AnalyticsQuerySerializer(serializers.Serializer):
    month = serializers.IntegerField(min_value=1, max_value=12, required=False)
    year = serializers.IntegerField(min_value=2000, max_value=2100, required=False)


class AnalyticsExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = ("id", "title", "amount", "expense_date", "category", "category_name")
