import os

from django.core.mail import send_mail

FROM_EMAIL = os.getenv("YANDEX_EMAIL_HOST_USER")


def send_course_update_email(course, emails_list):
    """Сервисная функция для отправки email-уведомлений подписчикам о том, что курс был обновлен.
    :param course: Объект Course, который обновился.
    :param emails_list: Список email-адресов получателей."""

    send_mail(
        subject="Обновление курса!",
        message=f"Здравствуйте! В курсе '{course.title}' появились новые материалы.",
        from_email=FROM_EMAIL,
        recipient_list=emails_list,
        fail_silently=False,
    )
