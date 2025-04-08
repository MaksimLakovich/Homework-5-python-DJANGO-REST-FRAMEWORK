from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Настройка отображения модели пользователя в админке."""

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
        ("Права доступа", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
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
