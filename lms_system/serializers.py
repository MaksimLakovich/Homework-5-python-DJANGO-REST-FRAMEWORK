from rest_framework import serializers

from lms_system.models import Course, Lesson
from lms_system.validators import YoutubeDomainValidator, validate_domain_links


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Lesson. Описывает то, какие поля модели Lesson будут участвовать в сериализации и десериализации.
    """

    class Meta:
        model = Lesson
        fields = "__all__"  # можно указать автоматом все поля модели
        validators = [
            YoutubeDomainValidator(fields=["video_url", "description"])
        ]


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Course. Описывает то, какие поля модели Course будут участвовать в сериализации и десериализации.
    """

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    description = serializers.CharField(validators=[validate_domain_links])

    def get_count_lessons(self, instance):
        """Функция для определения количества уроков в курсе. Запрос в БД для подсчёта связанных уроков."""
        return (
            instance.lessons.count()
        )  # Учитываю кастомный related_name="lessons" в модели Lesson

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "count_lessons",
            "lessons",
        ]  # можно указывать нужные поля модели
