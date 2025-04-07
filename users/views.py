from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser, Payments
from users.serializers import (
    CustomObtainPairSerializer,
    CustomUserSerializer,
    PaymentsSerializer,
)


class CustomUserListAPIView(generics.ListAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения списка зарегистрированных пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserCreateAPIView(generics.CreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для регистрации пользователя."""

    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения и редактирования профиля пользователя."""

    # Оптимизация работы - использование prefetch_related("payments"), что подтянет платежи одним SQL-запросом.
    # Это ускорит загрузку профиля, потому что платежи загрузятся за один SQL-запрос.
    queryset = CustomUser.objects.prefetch_related("payments").all()
    serializer_class = CustomUserSerializer


class CustomUserDestroyAPIView(generics.DestroyAPIView):
    """Класс-контроллер на основе базового Generic-класса для удаления пользователя."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Класс-контроллер на основе TokenObtainPairView для авторизации по email."""

    permission_classes = [AllowAny]
    serializer_class = CustomObtainPairSerializer


class PaymentsListCreateAPIView(generics.ListCreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения списка платежей и создания нового платежа."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

    # Бэкенд для обработки фильтра:
    filter_backends = [DjangoFilterBackend, OrderingFilter,]
    # Фильтрация по курсу, уроку и оплате:
    filterset_fields = ("paid_course", "paid_lesson", "payment_method",)
    # Сортировка по дате оплаты
    ordering_fields = ["payment_date"]


class PaymentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения, обновления и удаления одного платежа."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
