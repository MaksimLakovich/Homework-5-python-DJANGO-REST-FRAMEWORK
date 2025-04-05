from rest_framework import serializers

from lms_system.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Lesson. Описывает то, какие поля модели Lesson будут участвовать в сериализации и десериализации.
    """

    class Meta:
        model = Lesson
        fields = "__all__"  # можно указать автоматом все поля модели


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Course. Описывает то, какие поля модели Course будут участвовать в сериализации и десериализации.
    """

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

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
