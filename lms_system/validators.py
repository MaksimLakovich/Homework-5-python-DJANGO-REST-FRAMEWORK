from urllib.parse import urlparse

from rest_framework import serializers


class YoutubeDomainValidator:
    """Класс-валидатор для проверки допустимости домена в URL. Разрешает только ссылки
    на YouTube (youtube.com и www.youtube.com)."""

    allowed_domains = {"youtube.com", "www.youtube.com"}

    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        """Метод __call__() делает экземпляр класса вызываемым, как функцию.
        Используется в DRF как валидатор поля сериализатора."""
        value = attrs.get(self.field)
        if not value:
            return  # Пропускаю пустые значения
        # Лучше использовать urlparse из модуля urllib.parse, чтобы явно получить домен из URL.
        # Это надёжнее, чем просто искать подстроку "youtube.com" в полной ссылке, потому что могут быть
        # обманные случаи, например: "https://notyoutube.com/...", где "youtube.com" вроде бы присутствует в строке,
        # но на самом деле домен совсем другой. Если не извлекать домен отдельно, можно случайно принять такую
        # ссылку как допустимую.
        parsed_url = urlparse(value)
        domain = (
            parsed_url.netloc.lower()  # Это возвращает имя домена, а не всю строку целиком
        )
        if domain not in self.allowed_domains:
            raise serializers.ValidationError(
                {self.field: "Разрешены только ссылки на YouTube (youtube.com)."}
            )
