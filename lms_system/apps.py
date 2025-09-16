from django.apps import AppConfig


class LmsSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms_system'

    def ready(self):
        """Подключение сигналов в приложении (lms_system/signals.py).
        *** # noqa: F401*** - сигнализирует flake8, что мы сознательно оставляем "неиспользуемый импорт",
        чтоб проверка flake не выдавала ошибку. Это осознанный "ленивый" импорт: мы подключаем модуль сигналов
        внутри метода ready(), чтобы Django зарегистрировал их обработчики. Т.е., импорт нужен ради
        побочного эффекта (регистрации сигналов), а не ради использования переменной/функции."""
        import lms_system.signals  # noqa: F401
