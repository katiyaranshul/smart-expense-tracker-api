from rest_framework import serializers

from .models import Budget, Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description", "user", "created_at", "updated_at")
        read_only_fields = ("id", "user", "created_at", "updated_at")

    def validate_name(self, value):
        request = self.context["request"]
        queryset = Category.objects.filter(user=request.user, name__iexact=value.strip())
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("You already have a category with this name.")
        return value.strip()


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Expense
        fields = (
            "id",
            "title",
            "amount",
            "description",
            "expense_date",
            "category",
            "category_name",
            "user",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "category_name", "user", "created_at", "updated_at")

    def validate_category(self, category):
        request = self.context["request"]
        if category.user_id != request.user.id:
            raise serializers.ValidationError("Invalid category.")
        return category

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ("id", "month", "year", "limit_amount", "user", "created_at")
        read_only_fields = ("id", "user", "created_at")

    def validate_month(self, value):
        if value < 1 or value > 12:
            raise serializers.ValidationError("Month must be between 1 and 12.")
        return value

    def validate_limit_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget limit must be greater than zero.")
        return value

    def validate(self, attrs):
        request = self.context["request"]
        month = attrs.get("month", getattr(self.instance, "month", None))
        year = attrs.get("year", getattr(self.instance, "year", None))
        queryset = Budget.objects.filter(user=request.user, month=month, year=year)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("A budget already exists for this user and month.")
        return attrs
