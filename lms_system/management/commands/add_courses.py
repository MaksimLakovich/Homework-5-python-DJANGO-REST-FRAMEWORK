from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms_system.models import Course


class Command(BaseCommand):
    help = "Загрузка тестовых данных из фикстуры (courses)"

    def handle(self, *args, **kwargs):
        Course.objects.all().delete()
        call_command("loaddata", "data/courses.json")
        self.stdout.write(
            self.style.SUCCESS(
                "Успешно загружены тестовые данные из фикстуры (courses)"
            )
        )
