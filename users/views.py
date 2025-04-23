from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import CustomUser, Payments
from users.serializers import (
    CustomObtainPairSerializer,
    CustomUserSerializer,
    PaymentsSerializer,
)


class CustomUserListAPIView(generics.ListAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения списка зарегистрированных пользователей.
    Доступно: аутентифицированным пользователям."""

    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserCreateAPIView(generics.CreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для регистрации пользователя.
    Доступно: всем пользователям."""

    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения и редактирования профиля пользователя.
    Доступно:
    1) Просматривать профиль пользователя может любой авторизованный пользователь (только без персональных данных).
    2) Редактировать профиль пользователя может только сам пользователь."""

    # Оптимизация работы - использование prefetch_related("payments"), что подтянет платежи одним SQL-запросом.
    # Это ускорит загрузку профиля, потому что платежи загрузятся за один SQL-запрос.
    queryset = CustomUser.objects.prefetch_related("payments").all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        """Передаёт request в сериализатор для дальнейшего анализа (например, в to_representation)."""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def check_object_permissions(self, request, obj):
        """Проверяет права доступа к редактированию профиля.
        Доступно:
        1) Просматривать (GET) может любой авторизованный пользователь.
        2) Редактировать (PUT, PATCH) может только владелец профиля.
        Если пользователь пытается изменить чужой профиль, то вызывается отказ в доступе (HTTP 403)."""
        if request.method in ["PUT", "PATCH"] and request.user != obj:
            self.permission_denied(request, message="Можно редактировать только свой профиль.")
        return super().check_object_permissions(request, obj)


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
