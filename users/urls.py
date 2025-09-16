from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import (
    CustomTokenObtainPairView,
    CustomUserCreateAPIView,
    CustomUserDestroyAPIView,
    CustomUserListAPIView,
    CustomUserRetrieveUpdateAPIView,
    PaymentsListCreateAPIView,
    PaymentsRetrieveUpdateDestroyAPIView,
    StripePaymentStatusAPIView,
)

app_name = "users"

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", CustomUserCreateAPIView.as_view(), name="user-register"),
    path("users/", CustomUserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", CustomUserRetrieveUpdateAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/delete/", CustomUserDestroyAPIView.as_view(), name="user-delete"),
    path("payment/", PaymentsListCreateAPIView.as_view(), name="payment-list-create"),
    path("payment/<int:pk>/", PaymentsRetrieveUpdateDestroyAPIView.as_view(), name="payment-detail-delete"),
    path("payment/<int:pk>/status/", StripePaymentStatusAPIView.as_view(), name="payment-check-status"),
]
