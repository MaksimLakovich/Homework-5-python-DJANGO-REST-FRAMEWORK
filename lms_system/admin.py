from django.contrib import admin

from lms_system.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Настройка отображения данных модели Course в админке."""
    list_display = ("id", "title", "description",)
    list_filter = ("title",)
    search_fields = ("title", "description",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Настройка отображения данных модели Lesson в админке."""
    list_display = ("id", "course", "title", "description", "video_url",)
    list_filter = ("title",)
    search_fields = ("title", "description",)
