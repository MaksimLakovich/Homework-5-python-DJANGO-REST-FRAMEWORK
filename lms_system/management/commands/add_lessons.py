from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms_system.models import Lesson


class Command(BaseCommand):
    help = "Загрузка тестовых данных из фикстуры (lessons)"

    def handle(self, *args, **kwargs):
        Lesson.objects.all().delete()
        call_command("loaddata", "data/fixtures/lessons.json")
        self.stdout.write(
            self.style.SUCCESS(
                "Успешно загружены тестовые данные из фикстуры (lessons)"
            )
        )
