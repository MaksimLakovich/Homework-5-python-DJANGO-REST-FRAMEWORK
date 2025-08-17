from celery import shared_task  # type: ignore

from lms_system.models import Course, Subscription
from lms_system.services import send_course_update_email


@shared_task(bind=True, max_retries=3)
def task_send_course_update_email(self, course_id):
    """ Celery-задача: собирает список подписчиков курса и вызывает отправку писем.
    Шаги:
        1. Получает курс по ID.
        2. Находит всех подписчиков этого курса.
        3. Собирает список email-адресов.
        4. Если список не пустой - отправляет письма.
    :param course_id: ID обновленного курса."""
    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(course_id=course.pk).select_related("user")

        recipient_emails = []  # Создаю пустой список

        for sub in subscribers:  # Прохожусь по всем подпискам
            user = sub.user  # Беру связанного пользователя (уже подгружен из-за select_related)
            email = user.email  # Вытаскиваю его email

            if email:
                recipient_emails.append(email)

        if recipient_emails:
            send_course_update_email(course, recipient_emails)

    except Exception as e:
        # Повтор через 60 секунд, максимум 3 попытки согласно "max_retries=3"
        raise self.retry(exc=e, countdown=60)
