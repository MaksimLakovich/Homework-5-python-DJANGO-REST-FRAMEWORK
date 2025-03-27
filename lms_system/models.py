from django.db import models


class Course(models.Model):
    """Модель Course представляет Курс на платформе для онлайн-обучения."""
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

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.title}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]


class Lesson(models.Model):
    """Модель Lesson представляет Урок на платформе для онлайн-обучения."""
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

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title"]
