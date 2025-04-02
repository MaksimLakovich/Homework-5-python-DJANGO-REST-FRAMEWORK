from django.core.management import call_command
from django.core.management.base import BaseCommand

from users.models import Payments


class Command(BaseCommand):
    help = "Загрузка тестовых данных из фикстуры (payments)"

    def handle(self, *args, **kwargs):
        Payments.objects.all().delete()
        call_command("loaddata", "data/payments.json")
        self.stdout.write(
            self.style.SUCCESS(
                "Успешно загружены тестовые данные из фикстуры (payments)"
            )
        )
