from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms_system.models import Course, Lesson
from users.models import CustomUser


class LessonAPITestCase(APITestCase):
    """Тесты, которые будут проверять корректность работы CRUD для уроков (Lesson)."""

    def setUp(self):
        """Метод для подготовки тестовых данных и настроек перед выполнением тестов в тестовом классе."""
        # ШАГ 1: Создаю тестового пользователя (+ его же буду передавать в owner объектов Урок и Курс).
        # force_authenticate - выполняю аутентификацию клиента (исключить 401 Unauthorized), так как в настройках
        # проекта (settings.py): 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated']
        self.user = CustomUser.objects.create_user(
            email="user_1_for_tests@gmail.com", password="123qwe"
        )
        self.client.force_authenticate(user=self.user)
        # ШАГ 2: Создаю тестовый Курс:
        self.course = Course.objects.create(
            title="Какой-то тестовый курс",
            description="Какое-то тестовое описание",
            owner=self.user,
        )
        # ШАГ 3: Готовлю тестовые данные для Урока:
        self.data = {
            "course": self.course.pk,  # Подтягиваю ранее созданный тестовый Курс
            "title": "Введение в Django",
            "description": "Основы Django https://youtube.com/video.mp4 или http://youtube.com/video.mp4",
            "video_url": "https://youtube.com/video.mp4",
        }
        # ШАГ 4: Задаю базовый url, чтоб в части тестов с контроллером LessonListCreateAPIView не писать этот код:
        self.url = reverse("lms_system:lesson-list-create")

    def test_create_lesson(self):
        """Тест создания нового урока через POST-запрос."""
        response = self.client.post(
            self.url, self.data, format="json"
        )  # Отправляю POST-запрос
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Можно писать без ALL(),так как Django сам делает all() внутри count()
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(Lesson.objects.get().title, self.data["title"])
        self.assertEqual(Lesson.objects.get().owner, self.user)

    def test_read_list_lessons(self):
        """Тест получения списка уроков через GET-запрос."""
        # Создаю урок до отправки get-запроса на получение списка уроков
        Lesson.objects.create(
            course=self.course,
            title="Урок 1",
            description="Описание",
            video_url="https://youtube.com/lesson",
            owner=self.user,
        )
        response = self.client.get(self.url)  # Отправляю GET-запрос
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(len(response.data["results"]), 1)  # Проверяю наличие пагинации
        # Проверяю содержимое в списке и из-за того, что есть пагинация появляется "results".
        # Без пагинации было бы просто: response.data[0]["title"].
        self.assertEqual(response.data["results"][0]["title"], "Урок 1")

    def test_update_lesson(self):
        """Тест частичного обновления существующего урока через PATCH-запрос."""
        test_lesson = Lesson.objects.create(
            course=self.course,
            title="Урок 1",
            description="Описание",
            video_url="https://youtube.com/lesson",
            owner=self.user,
        )
        data = {
            "description": "Новые видео: https://youtube.com/video.mp4 или http://youtube.com/video.mp4"
        }
        # В данном тесте нельзя уже использовать базовый url из метода setUp() и поэтому устанавливаю нужные url в
        # самом тесте для вызова контроллера LessonRetrieveUpdateDestroyAPIView.
        # + передаю ID урока.
        url = reverse(
            "lms_system:lesson-retrieve-update-destroy", args=[test_lesson.pk]
        )
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.get().description, data["description"])

    def test_delete_lesson(self):
        """Тест удаления существующего урока через DELETE-запрос."""
        test_lesson = Lesson.objects.create(
            course=self.course,
            title="Урок 1",
            description="Описание",
            video_url="https://youtube.com/lesson",
            owner=self.user,
        )
        url = reverse(
            "lms_system:lesson-retrieve-update-destroy", args=[test_lesson.pk]
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_401_unauthenticated_create_lesson(self):
        """Тест создания урока неавторизованным пользователем (401 - Unauthorized)."""
        self.client.logout()  # Разлогиниваю пользователя
        response = self.client.post(
            self.url, self.data, format="json"
        )  # Отправляю POST-запрос
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_403_forbidden_update_lesson_by_stranger(self):
        """Тест проверки, что другой пользователь не может редактировать чужой урок (403 - Forbidden)."""
        # Шаг 1: Авторизованный пользователь №1 создаёт урок
        response = self.client.post(self.url, self.data, format="json")
        lesson_id = response.data["id"]  # Получаю ID созданного урока
        self.client.logout()  # Разлогиниваю пользователя №1

        # Шаг 2: Создаю пользователя №2
        stranger = CustomUser.objects.create_user(
            email="user_2_for_tests@gmail.com", password="123qwe123"
        )

        # Шаг 3: Пользователь №2 пытается изменить чужой урок
        update_data = {"description": "Новое видео: https://youtube.com/video_2.mp4"}
        self.client.force_authenticate(user=stranger)
        url = reverse("lms_system:lesson-retrieve-update-destroy", args=[lesson_id])
        response = self.client.patch(url, update_data, format="json")

        # Шаг 4: Проверка, что доступ запрещён
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_video_url(self):
        """Тест проверки, что ссылки кроме YouTube вызывают ошибку валидации."""
        data = {
            "course": self.course.pk,  # Подтягиваю ранее созданный тестовый Курс
            "title": "Введение в Django",
            "description": "Основы Django",
            "video_url": "https://not-youtube.com/video.mp4",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionToggleAPITestCase(APITestCase):
    """Тесты, которые будут проверять функционал работы подписки на обновления курса."""

    def setUp(self):
        """Метод для подготовки тестовых данных и настроек перед выполнением тестов в тестовом классе."""
        self.user = CustomUser.objects.create_user(
            email="user_1_for_tests@gmail.com", password="123qwe"
        )
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title="Какой-то тестовый курс",
            description="Какое-то тестовое описание",
            owner=self.user,
        )
        self.url = reverse("lms_system:subscription-toggle")
        self.data = {"course_id": self.course.pk}

    def test_user_subscribe_to_course(self):
        """Тест подписки пользователя на курс."""
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")

    def test_user_unsubscribe_from_course(self):
        """Тест отписки пользователя с курса."""
        self.client.post(self.url, self.data, format="json")
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
