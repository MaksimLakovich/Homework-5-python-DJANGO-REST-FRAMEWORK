from django.urls import path

from users.views import CustomUserRetrieveUpdateAPIView

app_name = "users"

urlpatterns = [
    path("profile/<int:pk>/", CustomUserRetrieveUpdateAPIView.as_view(), name="user-profile-retrieve-update")
]
