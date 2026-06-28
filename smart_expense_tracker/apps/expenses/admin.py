from django.contrib import admin

from .models import Budget, Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    search_fields = ("name", "user__username")
    list_filter = ("created_at",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "expense_date", "category", "user")
    search_fields = ("title", "category__name", "user__username")
    list_filter = ("expense_date", "category")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "month", "year", "limit_amount", "created_at")
    search_fields = ("user__username",)
    list_filter = ("month", "year")
