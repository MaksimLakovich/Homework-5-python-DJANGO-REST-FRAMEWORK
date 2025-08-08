from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomUser, Payments


class PaymentsSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Payments. Описывает то, какие поля модели Payments будут участвовать в сериализации и
    десериализации."""

    def validate(self, data):
        """Валидация данных для лучшего API-обслуживания - это ранняя валидация еще в сериализаторе поэтому из
        контроллера PaymentsListCreateAPIView() я перенес сюда эти проверки.
        Обоснование:
        - Если ошибка есть в теле запроса - то лучше её находить на уровне сериализатора, а не контроллера.
        - Так клиент (например, Postman или frontend) сразу получит 400 с объяснением, без лишней логики
        и без лишнего обращения к Stripe.
        :param data: Входные данные запроса для валидации (словарь validated_data).
        :return data: Валидированные данные (data), если нет ошибок.
        """
        paid_lesson = data.get("paid_lesson")
        paid_course = data.get("paid_course")

        if paid_course and paid_lesson:
            raise serializers.ValidationError(
                "Нельзя одновременно указать и Курс, и Урок. Выберите что-то одно."
            )

        if not paid_course and not paid_lesson:
            raise serializers.ValidationError(
                "Необходимо указать либо Курс, либо Урок."
            )

        return data

    class Meta:
        model = Payments
        fields = "__all__"
        # 1) Нельзя позволять клиенту вручную указывать stripe_product_id, stripe_price_id, stripe_session_id
        # и payment_url при создании платежа (эти поля должны быть read-only).
        # 2) Аналогично и user тоже должен задаваться только из request.user, а не из данных клиента
        read_only_fields = (
            "stripe_product_id",
            "stripe_price_id",
            "stripe_session_id",
            "payment_url",
            "user",
            "payment_date",
        )


class CustomUserSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели CustomUser. Описывает то, какие поля модели CustomUser будут участвовать в сериализации и
    десериализации."""

    payments = PaymentsSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        """Возвращает сериализованное представление пользователя.
        - Если запрашивающий пользователь смотрит "свой профиль", то отображаются все поля.
        - Если запрашивающий пользователь смотрит "чужой профиль", то скрываются конфиденциальные поля:
            - last_name (фамилия)
            - payments (история платежей)
            - password (в любом случае не нужен в ответе)
        Используется для динамической настройки отображения данных в зависимости от прав доступа.
        """

        representation = super().to_representation(instance)

        request = self.context.get("request")
        # "request.user != instance" - значит пользователь смотрит чужой профиль и нужно скрыть часть полей
        if request and request.user != instance:
            representation.pop("last_name", None)
            representation.pop("payments", None)
            representation.pop("password", None)

        return representation

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
            try:  # ШАГ 2: Ищу пользователя с таким email
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise AuthenticationFailed("Пользователь с таким email не найден.")

            if not user.check_password(password):  # ШАГ 3: Проверяю пароль
                raise AuthenticationFailed("Неверный пароль.")

        else:
            raise AuthenticationFailed("Необходимо указать email и пароль.")

        # ШАГ 4: Если все ок, то формирую словарь, чтобы передать в родительский "validate()"
        data = super().validate(
            {
                self.username_field: user.email,  # Ключ "email", значение - email пользователя
                "password": password,
            }
        )
        # ШАГ 5: Добавляю еще данные в ответ (опционально, это полезно для будущего функционала)
        data["email"] = user.email
        data["user_id"] = user.id

        return data
