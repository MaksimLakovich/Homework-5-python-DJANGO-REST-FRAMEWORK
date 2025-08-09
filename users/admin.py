from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Payments


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения модели *Пользователь* в админке."""

    list_display = ("email", "first_name", "last_name", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    # Группирует поля при редактировании пользователя:
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Персональная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "phone_number",
                    "city",
                )
            },
        ),
        (
            "Права доступа",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Даты", {"fields": ("last_login", "date_joined")}),
    )
    # Управляет полями при добавлении нового пользователя через админку
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    """Настройка отображения модели *Платежи* в админке."""

    list_display = (
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "payment_amount",
        "payment_method",
        "payment_status",
    )
    # *readonly_fields* для Stripe-полей это важный момент, потому что эти поля должны быть недоступны для ручного
    # редактирования. Админ сможет видеть эти поля, но не сможет их редактировать вручную.
    readonly_fields = (
        "payment_date",
        "payment_status",
        "stripe_product_id",
        "stripe_price_id",
        "stripe_session_id",
        "payment_url",
    )
    search_fields = (
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "payment_amount",
        "payment_method",
    )
    ordering = ("payment_date",)
