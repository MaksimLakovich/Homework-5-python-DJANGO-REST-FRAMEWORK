from django.core.management.base import BaseCommand
from users.models import CustomUser


class Command(BaseCommand):
    help = "Создание тестовых пользователей вручную через create_user()"

    def handle(self, *args, **kwargs):
        CustomUser.objects.filter(is_superuser=False).delete()
        users_data = [
            {
                "email": "ivan.petrov@gmail.com",
                "password": "123456asd",
                "phone_number": "+79991234567",
                "city": "Москва"
            },
            {
                "email": "elena.ivanova@gmail.com",
                "password": "123456zxc",
                "phone_number": "+79876543210",
                "city": "Санкт-Петербург"
            }
        ]

        for data in users_data:
            CustomUser.objects.create_user(**data)

        self.stdout.write(self.style.SUCCESS("Пользователи успешно созданы"))
