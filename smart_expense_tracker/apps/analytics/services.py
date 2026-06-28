import calendar
from decimal import Decimal

from django.db.models import Count, DecimalField, F, Sum, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.expenses.models import Budget, Expense


def _period(month=None, year=None):
    today = timezone.localdate()
    return int(month or today.month), int(year or today.year)


def _money(value):
    return value or Decimal("0.00")


def _sum_amount(alias="amount"):
    return Coalesce(
        Sum(alias),
        Value(Decimal("0.00")),
        output_field=DecimalField(max_digits=12, decimal_places=2),
    )


def monthly_summary(user, month=None, year=None):
    month, year = _period(month, year)
    summary = Expense.objects.filter(user=user, expense_date__month=month, expense_date__year=year).aggregate(
        total_expense=_sum_amount(),
        transaction_count=Count("id"),
    )
    return {
        "month": calendar.month_name[month],
        "year": year,
        "total_expense": _money(summary["total_expense"]),
        "transaction_count": summary["transaction_count"],
    }


def category_summary(user, month=None, year=None):
    month, year = _period(month, year)
    rows = (
        Expense.objects.filter(user=user, expense_date__month=month, expense_date__year=year)
        .values(category_name=F("category__name"))
        .annotate(total=_sum_amount())
        .order_by("-total")
    )
    return [{"category": row["category_name"], "total": row["total"]} for row in rows]


def top_expenses(user, limit=5, month=None, year=None):
    month, year = _period(month, year)
    return Expense.objects.select_related("category").filter(
        user=user,
        expense_date__month=month,
        expense_date__year=year,
    ).order_by("-amount")[:limit]


def budget_status(user, month=None, year=None):
    month, year = _period(month, year)
    spent = _money(
        Expense.objects.filter(user=user, expense_date__month=month, expense_date__year=year).aggregate(
            total=_sum_amount()
        )["total"]
    )
    budget = Budget.objects.filter(user=user, month=month, year=year).first()
    limit = budget.limit_amount if budget else Decimal("0.00")
    remaining = limit - spent
    percentage_used = None if limit == 0 else round((spent / limit) * Decimal("100"), 2)

    return {
        "month": calendar.month_name[month],
        "year": year,
        "budget_limit": limit,
        "total_spent": spent,
        "remaining_amount": remaining,
        "percentage_used": percentage_used,
    }
