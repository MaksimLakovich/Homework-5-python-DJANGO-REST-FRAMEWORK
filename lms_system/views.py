from rest_framework import generics, viewsets

from lms_system.models import Course, Lesson
from lms_system.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Автоматический CRUD для модели Course."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения списка уроков и создания нового урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения, обновления и удаления одного урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
