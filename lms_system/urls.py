from django.urls import path
from rest_framework.routers import DefaultRouter

from lms_system.views import (CourseViewSet, LessonListCreateAPIView,
                              LessonRetrieveUpdateDestroyAPIView, SubscriptionToggleAPIView)

app_name = "lms_system"

# Описание маршрутизации для ViewSet
router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/", LessonListCreateAPIView.as_view(), name="lesson-list-create"),
    path("lesson/<int:pk>/", LessonRetrieveUpdateDestroyAPIView.as_view(), name="lesson-retrieve-update-destroy"),
    path("subscriptions/", SubscriptionToggleAPIView.as_view(), name="subscription-toggle"),
] + router.urls
