from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common.responses import success_response
from apps.common.schema import (
    ERROR_RESPONSE_EXAMPLE,
    LOGIN_REQUEST_EXAMPLE,
    LOGIN_RESPONSE_EXAMPLE,
    REGISTER_REQUEST_EXAMPLE,
    SUCCESS_RESPONSE_EXAMPLE,
)

from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Register a user",
    description="Create a new account. Email addresses must be unique.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(response=UserProfileSerializer, examples=[SUCCESS_RESPONSE_EXAMPLE]),
        400: OpenApiResponse(description="Validation failed", examples=[ERROR_RESPONSE_EXAMPLE]),
    },
    examples=[REGISTER_REQUEST_EXAMPLE, SUCCESS_RESPONSE_EXAMPLE],
)
class RegisterAPIView(generics.CreateAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserProfileSerializer(user).data
        return success_response("User registered successfully", data, status.HTTP_201_CREATED)


@extend_schema(
    tags=["Authentication"],
    summary="Login",
    description="Obtain JWT access and refresh tokens using username and password.",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(description="JWT tokens", examples=[LOGIN_RESPONSE_EXAMPLE]),
        401: OpenApiResponse(description="Invalid credentials", examples=[ERROR_RESPONSE_EXAMPLE]),
    },
    examples=[LOGIN_REQUEST_EXAMPLE, LOGIN_RESPONSE_EXAMPLE],
)
class LoginAPIView(TokenObtainPairView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response("Login successful", response.data, response.status_code)


@extend_schema(
    tags=["Authentication"],
    summary="Refresh access token",
    description="Exchange a valid refresh token for a new access token.",
)
class RefreshTokenAPIView(TokenRefreshView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return success_response("Token refreshed successfully", response.data, response.status_code)


@extend_schema(
    tags=["Authentication"],
    summary="Get profile",
    description="Return the authenticated user's profile.",
    responses={200: OpenApiResponse(response=UserProfileSerializer, examples=[SUCCESS_RESPONSE_EXAMPLE])},
    examples=[SUCCESS_RESPONSE_EXAMPLE],
)
class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return success_response("Profile retrieved successfully", serializer.data)
