from rest_framework import serializers

from lms_system.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Course. Описывает то, какие поля модели Course будут участвовать в сериализации и десериализации."""

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description",]  # можно указывать нужные поля модели


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на
    основе модели Lesson. Описывает то, какие поля модели Lesson будут участвовать в сериализации и десериализации."""

    class Meta:
        model = Lesson
        fields = "__all__"  # можно указать автоматом все поля модели
