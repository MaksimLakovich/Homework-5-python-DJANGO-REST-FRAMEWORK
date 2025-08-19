from django.db import models


class TimeStampedModel(models.Model):
    """Абстрактная базовая модель для дальнейшего создания *created_at* и *updated_at* во всех моделях приложения."""

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания:",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления:",
    )

    class Meta:
        abstract = True


class Course(TimeStampedModel):
    """Модель Course представляет Курс на платформе для онлайн-обучения.
    Наследуется от абстрактной базовой модели TimeStampedModel для добавления created_at и updated_at по умолчанию."""

    title = models.CharField(
        max_length=500,
        unique=True,
        verbose_name="Название курса:",
        help_text="Введите название",
    )
    preview = models.ImageField(
        upload_to="course_preview",
        blank=True,
        null=True,
        verbose_name="Превью (картинка) курса:",
        help_text="Загрузите картинку",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса:",
        help_text="Укажите описание",
    )
    owner = models.ForeignKey(
        # Использую строку в to="users.CustomUser" (рекомендуется для ForeignKey к User) вместо to=CustomUser, чтоб
        # избежать ошибки циклического импорта (circular import), которая возникает из-за того, что
        # в "users/models.py" уже есть "from lms_system.models import Course, Lesson"
        to="users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_courses",
        verbose_name="Владелец:",
        help_text="Укажите пользователя, создавшего курс",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


class Lesson(TimeStampedModel):
    """Модель Lesson представляет Урок на платформе для онлайн-обучения.
    Наследуется от абстрактной базовой модели TimeStampedModel для добавления created_at и updated_at по умолчанию."""

    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс:",
        help_text="Выберите курс",
    )
    title = models.CharField(
        max_length=500,
        unique=True,
        verbose_name="Название урока:",
        help_text="Введите название",
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока:",
        help_text="Укажите описание",
    )
    preview = models.ImageField(
        upload_to="lesson_preview",
        blank=True,
        null=True,
        verbose_name="Превью (картинка) урока:",
        help_text="Загрузите картинку",
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Видео урока:",
        help_text="Загрузите видео",
    )
    owner = models.ForeignKey(
        # Использую строку в to="users.CustomUser" (рекомендуется для ForeignKey к User) вместо to=CustomUser, чтоб
        # избежать ошибки циклического импорта (circular import), которая возникает из-за того, что
        # в "users/models.py" уже есть "from lms_system.models import Course, Lesson"
        to="users.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_lessons",
        verbose_name="Владелец:",
        help_text="Укажите пользователя, создавшего урок",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]


class Subscription(models.Model):
    """Модель Subscription представляет Подписку на обновление курса (Course) для пользователя (CustomUser)."""

    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",  # Позволяет получить список всех подписок на курс: course.subscriptions.all()
        verbose_name="Курс подписки:",
        help_text="Укажите курс подписки",
    )
    user = models.ForeignKey(
        to="users.CustomUser",
        on_delete=models.CASCADE,
        related_name="subscribed_courses",  # Позволяет получить список курсов, на которые подписан пользователь
        verbose_name="Подписчик:",
        help_text="Укажите подписчика",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"Пользователь {self.user} подписан на {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["course"]
