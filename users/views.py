from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter

from users.models import CustomUser, Payments
from users.serializers import CustomUserSerializer, PaymentsSerializer


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Класс-контроллер на основе базового Generic-класса для редактирования профилей любых пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


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
    # ordering = ["-payment_date"]  # По умолчанию сортировка от новых к старым


class PaymentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения, обновления и удаления одного платежа."""

    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer
