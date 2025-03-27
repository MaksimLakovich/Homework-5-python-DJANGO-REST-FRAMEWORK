from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField  # type: ignore


class CustomUser(AbstractUser):
    """Модель CustomUser представляет пользователя на платформе для онлайн-обучения."""

    username = None  # type: ignore
    email = models.EmailField(
        unique=True,
        verbose_name="Почта (username):",
        help_text="Введите email",
    )
    phone_number = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name="Телефон:",
        help_text="Введите телефон"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Город:",
        help_text="Укажите город",
    )
    avatar = models.ImageField(
        upload_to="user_avatar",
        blank=True,
        null=True,
        verbose_name="Аватар:",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]
