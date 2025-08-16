from django.db.models.signals import post_save
from django.dispatch import receiver

from lms_system.models import Lesson


@receiver(post_save, sender=Lesson)
def update_course_timestamp(sender, instance, **kwargs):
    """Сигнал для обновления в объекте Course значения поля *updated_at*,
     если было выполнено обновление объекта Lesson, который входит в данный Курс."""
    instance.course.save(update_fields=["updated_at"])
