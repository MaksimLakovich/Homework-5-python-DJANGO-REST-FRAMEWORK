from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from lms_system.models import Course, Lesson


@receiver(post_save, sender=Lesson)
def update_course_timestamp(sender, instance, **kwargs):
    """Сигнал для обновления в объекте Course значения поля *updated_at*, если:
     1) было выполнено обновление существующего объекта Lesson, который входит в данный Курс.
     2) или был создан новый объект Lesson, который входит в данный Курс."""
    # Это альтернативный вариант вместо "instance.course.save(update_fields=["updated_at"])" - без загрузки
    # объекта Course. Тут мы делаем все одним UPDATE-запросом и вообще не загружаем Course в память.
    # Плюсы: один UPDATE, без SELECT и без вызова save(), а значит не сработают сигналы для Course, если они появятся.
    # Минус: руками выставляем timezone.now(), обходя auto_now=True, но в этом кейсе это нормально и ничего не портит.
    Course.objects.filter(pk=instance.course_id).update(updated_at=timezone.now())
