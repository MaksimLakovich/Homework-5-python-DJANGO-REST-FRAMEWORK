from django.apps import AppConfig


class LmsSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lms_system'

    def ready(self):
        """Подключение сигналов в приложении (lms_system/signals.py)."""
        import lms_system.signals
