from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser, Payments


class PaymentsSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Payments. Описывает то, какие поля модели Payments будут участвовать в сериализации и
    десериализации."""

    class Meta:
        model = Payments
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели CustomUser. Описывает то, какие поля модели CustomUser будут участвовать в сериализации и
    десериализации."""

    payments = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        # extra_kwargs - это зарезервированное имя в Meta-классе ModelSerializer для настройки конкретных полей,
        # например, ниже указываю что пароль только на ЗАПИСЬ. Т.е. его можно отправить через POST/PUT/PATCH,
        # но оно не будет отображаться в ответе API (GET, LIST и т.п.).
        extra_kwargs = {
            "password": {"write_only": True},
        }


class CustomObtainPairSerializer(TokenObtainPairSerializer):
    """Кастомный класс-сериализатор токена наследующийся от TokenObtainPairSerializer, позволяющий вход по email."""

    # ВАЖНО! Необходимо указать, что username_field - это будет email.
    # До это мы указывали в модели это "USERNAME_FIELD = "email"" но это настройка Django, например, в админке,
    # логике логина, командах createsuperuser и т.п. Но это не влияет на процессы DRF. Логика сериализатора от
    # DRF Simple JWT НЕ смотрит на USERNAME_FIELD модели автоматически. Поэтому чтобы Simple JWT понял, что логин
    # должен быть по email, а не по username, нужно явно указать это в сериализаторе в username_field
    username_field = CustomUser.EMAIL_FIELD

    def validate(self, attrs):
        email = attrs.get("email")  # получаю email и password из тела запроса
        password = attrs.get("password")

        if email and password:  # ШАГ 1: проверяю все ли данные есть
            try:
                user = CustomUser.objects.get(email=email)  # ШАГ 2: Ищу пользователя с таким email
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Пользователь с таким email не найден.")

            if not user.check_password(password):  # ШАГ 3: Проверяю пароль
                raise AuthenticationFailed("Неверный пароль.")

        else:
            raise AuthenticationFailed("Необходимо указать email и пароль.")

        # ШАГ 4: Если все ок, то формирую словарь, чтобы передать в родительский "validate()"
        data = super().validate({
            self.username_field: user.email,  # Ключ "email", значение - email пользователя
            "password": password
        })
        # ШАГ 5: Добавляю еще данные в ответ (опционально, это полезно для будущего функционала)
        data["email"] = user.email
        data["user_id"] = user.id

        return data
