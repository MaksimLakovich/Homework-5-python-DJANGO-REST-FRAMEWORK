from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from lms_system.models import Course, Lesson
from lms_system.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator


class CourseViewSet(viewsets.ModelViewSet):
    """Автоматический CRUD для модели Course на основе ModelViewSet."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        """Определяет права доступа к действиям с курсами в зависимости от типа запроса (action).
        - list / retrieve / update / partial_update:
            Доступ разрешён для модераторов, администраторов и просто аутентифицированных пользователей.
            Модераторы не могут создавать или удалять, но могут просматривать и редактировать.
        - create / destroy:
            Только для администраторов (например, суперпользователь).
        Возвращает список активных permission-классов."""

        if self.action in ["list", "retrieve", "update", "partial_update"]:
            self.permission_classes = [IsModerator | IsAdminUser | IsAuthenticated]
        elif self.action in ["create", "destroy"]:
            self.permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения списка уроков и создания нового урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """Определяет права доступа к действиям со списком и созданием уроков:
        - GET (список - List): доступен модераторам, администраторам и просто аутентифицированных пользователей;
        - POST (создание - Create): доступен только администраторам (например, суперпользователь).
        Возвращает соответствующий список permission-классов."""

        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsModerator | IsAdminUser | IsAuthenticated]
        return [permission() for permission in self.permission_classes]


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения, обновления и удаления одного урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """Определяет права доступа к действиям с конкретным уроком:
        - GET (просмотр - Retrieve), PUT/PATCH (обновление - Update): доступны модераторам, администраторам и
        просто аутентифицированных пользователей;
        - DELETE (удаление - Destroy): доступно только администраторам (например, суперпользователь).
        Возвращает соответствующий список permission-классов."""

        if self.request.method == "DELETE":
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsModerator | IsAdminUser | IsAuthenticated]
        return [permission() for permission in self.permission_classes]
