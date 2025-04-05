from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загрузка тестовых данных из фикстуры (users)"

    def handle(self, *args, **kwargs):
        call_command("loaddata", "data/users.json")
        self.stdout.write(
            self.style.SUCCESS(
                "Успешно загружены тестовые данные из фикстуры (users)"
            )
        )
