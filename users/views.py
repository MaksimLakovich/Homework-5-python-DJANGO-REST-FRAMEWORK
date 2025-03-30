from rest_framework import generics

from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Класс-контроллер на основе базового Generic-класса для редактирования профилей любых пользователей."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
