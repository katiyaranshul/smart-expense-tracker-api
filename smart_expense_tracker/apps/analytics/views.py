from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework.views import APIView

from apps.common.responses import success_response
from apps.common.schema import AUTH_HEADER_EXAMPLE, SUCCESS_RESPONSE_EXAMPLE

from .serializers import (
    AnalyticsExpenseSerializer,
    AnalyticsQuerySerializer,
    BudgetStatusSerializer,
    CategorySummaryItemSerializer,
    MonthlySummarySerializer,
)
from .services import budget_status, category_summary, monthly_summary, top_expenses


ANALYTICS_QUERY_PARAMETERS = [
    OpenApiParameter(name="month", type=int, location=OpenApiParameter.QUERY, required=False, description="Month number (1-12)."),
    OpenApiParameter(name="year", type=int, location=OpenApiParameter.QUERY, required=False, description="Four-digit year."),
]


class AnalyticsBaseAPIView(APIView):
    def get_period(self, request):
        serializer = AnalyticsQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data.get("month"), serializer.validated_data.get("year")


@extend_schema(
    tags=["Analytics"],
    summary="Monthly spending summary",
    description="Return total spending and transaction count for a month. Defaults to the current month.",
    parameters=ANALYTICS_QUERY_PARAMETERS,
    responses={200: OpenApiResponse(response=MonthlySummarySerializer, examples=[SUCCESS_RESPONSE_EXAMPLE])},
    examples=[AUTH_HEADER_EXAMPLE],
)
class MonthlyAnalyticsAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        data = monthly_summary(request.user, month, year)
        return success_response("Monthly analytics retrieved successfully", data)


@extend_schema(
    tags=["Analytics"],
    summary="Category spending summary",
    description="Return spending totals grouped by category for the selected month.",
    parameters=ANALYTICS_QUERY_PARAMETERS,
    responses={200: OpenApiResponse(response=CategorySummaryItemSerializer(many=True), examples=[SUCCESS_RESPONSE_EXAMPLE])},
    examples=[AUTH_HEADER_EXAMPLE],
)
class CategoryAnalyticsAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        data = category_summary(request.user, month, year)
        return success_response("Category analytics retrieved successfully", data)


@extend_schema(
    tags=["Analytics"],
    summary="Top expenses",
    description="Return the highest expenses for the selected month.",
    parameters=ANALYTICS_QUERY_PARAMETERS,
    responses={200: OpenApiResponse(response=AnalyticsExpenseSerializer(many=True), examples=[SUCCESS_RESPONSE_EXAMPLE])},
    examples=[AUTH_HEADER_EXAMPLE],
)
class TopExpensesAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        expenses = top_expenses(request.user, month=month, year=year)
        data = AnalyticsExpenseSerializer(expenses, many=True).data
        return success_response("Top expenses retrieved successfully", data)


@extend_schema(
    tags=["Analytics"],
    summary="Budget status",
    description="Compare monthly spending against the user's budget limit.",
    parameters=ANALYTICS_QUERY_PARAMETERS,
    responses={200: OpenApiResponse(response=BudgetStatusSerializer, examples=[SUCCESS_RESPONSE_EXAMPLE])},
    examples=[AUTH_HEADER_EXAMPLE],
)
class BudgetStatusAPIView(AnalyticsBaseAPIView):
    def get(self, request):
        month, year = self.get_period(request)
        data = budget_status(request.user, month, year)
        return success_response("Budget status retrieved successfully", data)
