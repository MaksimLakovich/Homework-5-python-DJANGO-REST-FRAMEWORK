from rest_framework import serializers

from users.models import CustomUser, Payments


class CustomUserSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели CustomUser. Описывает то, какие поля модели CustomUser будут участвовать в сериализации и
    десериализации."""

    class Meta:
        model = CustomUser
        fields = "__all__"  # кроме password нужно сделать, чтоб нельзя было просто редактировать его


class PaymentsSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Payments. Описывает то, какие поля модели Payments будут участвовать в сериализации и
    десериализации."""

    class Meta:
        model = Payments
        fields = "__all__"
