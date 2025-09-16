from django.contrib import admin

from lms_system.models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Настройка отображения данных модели Course в админке."""

    list_display = (
        "id",
        "title",
        "description",
        "created_at",
        "updated_at",
    )
    list_filter = ("title",)
    search_fields = (
        "title",
        "description",
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Настройка отображения данных модели Lesson в админке."""

    list_display = (
        "id",
        "course",
        "title",
        "description",
        "video_url",
        "created_at",
        "updated_at",
    )
    list_filter = ("title",)
    search_fields = (
        "title",
        "description",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Настройка отображения данных модели Subscription в админке."""

    list_display = (
        "id",
        "course_id",
        "user_id",
    )
    list_filter = (
        "course_id",
        "user_id",
    )
    search_fields = (
        "course_id",
        "user_id",
    )
