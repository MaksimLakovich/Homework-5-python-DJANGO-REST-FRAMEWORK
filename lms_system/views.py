from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms_system.models import Course, Lesson, Subscription
from lms_system.paginators import ListPagination
from lms_system.serializers import CourseSerializer, LessonSerializer
from lms_system.tasks import task_send_course_update_email
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    """Автоматический CRUD для модели Course на основе ModelViewSet."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = ListPagination

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


    def perform_update(self, serializer):
        """При обновлении курса запускает Celery-задачу для уведомления подписчиков."""
        course = serializer.save()
        task_send_course_update_email.delay(course.pk)


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """Класс-контроллер на основе базового Generic-класса для получения списка уроков и создания нового урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = ListPagination

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


class SubscriptionToggleAPIView(APIView):
    """Класс-контроллер на основе низкоуровневого APIView для подписки/отписки Пользователя на Курс."""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Метод для подписки/отписки Пользователя на Курс.
        1. Получает пользователя из request.user (аутентифицированный пользователь).
        2. Получает ID курса из request.data.
        3. Проверяет, есть ли уже подписка на курс для этого пользователя.
            - если есть, то удаляет её (отписка).
            - если нет, то создаёт новую (подписка).
        4. Возвращает JSON-ответ с сообщением."""
        obj_user = (
            request.user
        )  # Получаю объект текущего авторизованного пользователя (CustomUser) из запроса
        course_id = request.data.get(
            "course_id"
        )  # Получаю ID курса из запроса (из тела POST-запроса)

        if not course_id:
            return Response({"error": "Не указан id курса"}, status=400)

        # Ищу в БД курс по id, а если такого курса нет, то возвращаю 404:
        obj_course = get_object_or_404(Course, id=course_id)

        # Получаю QuerySet с существующей подпиской (если она есть). Когда вызываю filter(user=user) и передаю
        # туда объект целиком, Django автоматически использует его первичный ключ (ID). Но можно в фильтр передавать
        # id напрямую. Это будет равносильными запросами. Итого:
        # 1) "filter(user=user)" - если нужно передать объект модели, а Django сам достанет .pk (или .id).
        # 2) "filter(user=user.pk)" - если передаю только id (user.pk) или просто число (user=3), он использует его.
        subscription_data = Subscription.objects.filter(
            user=obj_user.pk, course=obj_course.pk
        )

        if subscription_data.exists():
            subscription_data.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=obj_user, course=obj_course)
            message = "Подписка добавлена"
        return Response({"message": message})  # Возвращаю JSON-ответ
