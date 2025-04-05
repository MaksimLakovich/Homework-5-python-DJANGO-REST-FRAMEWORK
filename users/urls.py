from django.urls import path

from users.views import (
    CustomUserRetrieveUpdateAPIView,
    PaymentsListCreateAPIView,
    PaymentsRetrieveUpdateDestroyAPIView,
)

app_name = "users"

urlpatterns = [
    path(
        "profile/<int:pk>/",
        CustomUserRetrieveUpdateAPIView.as_view(),
        name="user-profile-retrieve-update",
    ),
    path(
        "payment/",
         PaymentsListCreateAPIView.as_view(),
         name="payment-list-create",
    ),
    path(
        "payment/<int:pk>/",
        PaymentsRetrieveUpdateDestroyAPIView.as_view(),
        name="payment-retrieve-update-destroy",
    ),
]
