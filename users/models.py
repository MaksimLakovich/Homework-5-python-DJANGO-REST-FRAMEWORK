from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField  # type: ignore

from lms_system.models import Course, Lesson
from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    """Модель CustomUser представляет пользователя на платформе для онлайн-обучения (авторизация по email)."""

    username = None  # type: ignore
    email = models.EmailField(
        unique=True,
        verbose_name="Почта (username):",
        help_text="Введите email",
    )
    phone_number = PhoneNumberField(
        blank=True, null=True, verbose_name="Телефон:", help_text="Введите телефон"
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

    # Указываю кастомный менеджер для пользователя без поля username.
    # Указываю "type: ignore" чтоб убрать ошибку типизации mypy, так как пока не разобрался как правильно
    # работать с типизацией TypeVar.
    objects = CustomUserManager()  # type: ignore

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["email"]


class Payments(models.Model):
    """Модель Payments представляет платежи за Lesson и/или за Course на платформе для онлайн-обучения."""

    METHOD = [
        ("transfer", "Перевод на счет"),
        ("cash", "Наличные"),
    ]

    user = models.ForeignKey(
        to=CustomUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments",
        verbose_name="Пользователь:",
        help_text="Укажите пользователя",
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время оплаты:",
        help_text="Укажите дату и время оплаты",
    )
    paid_course = models.ForeignKey(
        to=Course,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments_for_courses",
        verbose_name="Оплаченный курс:",
        help_text="Укажите оплаченный курс",
    )
    paid_lesson = models.ForeignKey(
        to=Lesson,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="payments_for_lessons",
        verbose_name="Оплаченный урок:",
        help_text="Укажите оплаченный урок",
    )
    payment_amount = models.FloatField(
        blank=False,
        null=False,
        verbose_name="Сумма платежа:",
        help_text="Укажите сумму платежа",
    )
    payment_method = models.CharField(
        max_length=100,
        choices=METHOD,
        verbose_name="Метод платежа:",
        help_text="Укажите метод платежа",
    )
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Созданный продукт в платежной системе Stripe:",
    )
    stripe_price_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Созданная цена в платежной системе Stripe:",
    )
    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Созданная сессия для получения ссылки в платежной системе Stripe:",
    )
    payment_url = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="Ссылка на оплату продукта:",
    )

    def __str__(self):
        """Метод определяет строковое представление объекта. Полезно для отображения объектов в админке/консоли."""
        return f"Платеж от {self.user.email} на сумму {self.payment_amount} / {self.payment_date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
