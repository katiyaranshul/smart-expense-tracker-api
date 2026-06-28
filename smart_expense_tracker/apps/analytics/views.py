from rest_framework.views import APIView

from apps.common.responses import success_response

from .serializers import AnalyticsExpenseSerializer, AnalyticsQuerySerializer
from .services import budget_status, category_summary, monthly_summary, top_expenses


class AnalyticsBaseAPIView(APIView):
    def get_period(self, request):
        serializer = AnalyticsQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data.get("month"), serializer.validated_data.get("year")


class MonthlyAnalyticsAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        data = monthly_summary(request.user, month, year)
        return success_response("Monthly analytics retrieved successfully", data)


class CategoryAnalyticsAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        data = category_summary(request.user, month, year)
        return success_response("Category analytics retrieved successfully", data)


class TopExpensesAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        expenses = top_expenses(request.user, month=month, year=year)
        data = AnalyticsExpenseSerializer(expenses, many=True).data
        return success_response("Top expenses retrieved successfully", data)


class BudgetStatusAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        data = budget_status(request.user, month, year)
        return success_response("Budget status retrieved successfully", data)
