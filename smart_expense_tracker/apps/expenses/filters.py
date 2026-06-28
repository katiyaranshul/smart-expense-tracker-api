import django_filters

from .models import Expense


class ExpenseFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(field_name="category_id")
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    start_date = django_filters.DateFilter(field_name="expense_date", lookup_expr="gte")
    end_date = django_filters.DateFilter(field_name="expense_date", lookup_expr="lte")

    class Meta:
        model = Expense
        fields = ["category", "min_amount", "max_amount", "start_date", "end_date"]
