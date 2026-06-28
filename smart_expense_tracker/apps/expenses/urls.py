from rest_framework.routers import DefaultRouter

from .views import BudgetViewSet, CategoryViewSet, ExpenseViewSet


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("expenses", ExpenseViewSet, basename="expense")
router.register("budgets", BudgetViewSet, basename="budget")

urlpatterns = router.urls
