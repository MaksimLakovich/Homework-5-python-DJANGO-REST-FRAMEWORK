from rest_framework import serializers

from lms_system.models import Course, Lesson, Subscription
from lms_system.validators import YoutubeDomainValidator, validate_domain_links


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Lesson. Описывает то, какие поля модели Lesson будут участвовать в сериализации и десериализации.
    """

    class Meta:
        model = Lesson
        fields = "__all__"  # можно указать автоматом все поля модели
        validators = [YoutubeDomainValidator(fields=["video_url", "description"])]


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Course. Описывает то, какие поля модели Course будут участвовать в сериализации и десериализации.
    """

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    description = serializers.CharField(validators=[validate_domain_links])
    is_subscribed = serializers.SerializerMethodField()

    def get_count_lessons(self, instance):
        """Функция для определения количества уроков в курсе. Запрос в БД для подсчёта связанных уроков."""
        return (
            instance.lessons.count()
        )  # Учитываю кастомный related_name="lessons" в модели Lesson

    def get_is_subscribed(self, instance):
        """Функция для проверки подписан ли текущий пользователь на данный курс (instance).
        1. Получает объект request из контекста сериализатора. Это передаётся автоматически при
        использовании APIView, ViewSet, GenericAPIView. Контекст сериализатора будет уже включать request. через
        `get_serializer_context()`.
        2. Проверяет, аутентифицирован ли пользователь.
        3. Выполняет фильтрацию по модели Subscription.
            - если запись найдена, то возвращает True.
            - если не найдена, то возвращает False."""
        request = self.context.get("request")

        if request and request.user and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=instance
            ).exists()
        return False

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "count_lessons",
            "lessons",
            "is_subscribed",
        ]  # можно указывать нужные поля модели
