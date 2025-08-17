from datetime import timedelta

from celery import shared_task  # type: ignore
from django.utils import timezone

from users.models import CustomUser


@shared_task()
def task_deactivate_inactive_users():
    """ Celery-задача: проверяет пользователей по дате последнего входа по полю last_login и, если пользователь
    не заходил более месяца, блокировать его с помощью флага is_active."""
    month_ago = timezone.now() - timedelta(days=30)  # Определяю какая дата была на этот момент ровно 30 дней назад
    users_for_deactivate = CustomUser.objects.filter(last_login__lt=month_ago, is_active=True)  # Получаю QuerySet
    # Массовое обновление на уровне БД в один SQL-запрос. Обновление касается всех строк, которые подходят
    # под условия QuerySet-а:
    users_for_deactivate.update(is_active=False)
