from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from lms_system.models import Course, Lesson
from lms_system.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Автоматический CRUD для модели Course на основе ModelViewSet."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        """Определяет права доступа к действиям с курсами в зависимости от типа запроса (action).
        - create / list:
            Доступ разрешён только администраторам (IsAdminUser) и аутентифицированным (IsAuthenticated).
            Владелец курса назначается автоматически (self.request.user).
        - retrieve / update / partial_update:
            Владелец курса (IsOwner) может просматривать и редактировать свои курсы.
            Модератор (IsModerator) может просматривать и редактировать любые курсы.
        - destroy:
            Только владелец курса может удалить свой курс.
            Администратор (IsAdminUser) может удалять любые курсы.
        Возвращает список активных permission-классов в зависимости от действия."""

        if self.action in ["create", "list"]:
            self.permission_classes = [IsAuthenticated | IsAdminUser]
        elif self.action in ["retrieve", "update", "partial_update"]:
            self.permission_classes = [IsAuthenticated & IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated & IsOwner | IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Определяет и фиксирует владельцем Пользователя, который создал данный объект."""

        serializer.save(owner=self.request.user)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения списка уроков и создания нового урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """Определяет права доступа к действиям со списком и созданием уроков:
        - GET (список - List), POST (создание - Create):
            Доступ разрешён только администраторам (IsAdminUser) и аутентифицированным (IsAuthenticated).
            Владелец урока назначается автоматически (self.request.user).
        Возвращает соответствующий список permission-классов."""

        if self.request.method in ["GET", "POST"]:
            self.permission_classes = [IsAuthenticated | IsAdminUser]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Присваивает текущего авторизованного пользователя как владельца (owner) создаваемого объекта."""

        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения, обновления и удаления одного урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """Определяет права доступа к действиям с конкретным уроком:
        - GET (просмотр - Retrieve), PUT/PATCH (обновление - Update):
            Владелец урока (IsOwner) может просматривать и редактировать свои уроки.
            Модератор (IsModerator) может просматривать и редактировать любые уроки.
        - DELETE (удаление - Destroy):
            Только владелец урока может удалить свой урок.
            Администратор (IsAdminUser) может удалять любые уроки.
        Возвращает список активных permission-классов в зависимости от действия."""

        if self.request.method == "DELETE":
            self.permission_classes = [IsAuthenticated & IsOwner | IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticated & IsOwner | IsModerator]
        return [permission() for permission in self.permission_classes]
