import re
from urllib.parse import urlparse

from rest_framework import serializers


class YoutubeDomainValidator:
    """Класс-валидатор для проверки допустимости домена в передаваемых пользователями URL. Разрешает только ссылки
    на YouTube (youtube.com и www.youtube.com)."""

    allowed_domains = {"youtube.com", "www.youtube.com"}

    def __init__(self, fields):
        """Метод __init__(self, field) необходим для того, чтобы понимать к какому полю относится валидатор. Потому что
        по условию ДЗ я потом должен использовать валидатор в "class Meta" у сериализатора LessonSerializer,
        а "class Meta" работает только с ОДНИМ полем всегда, а не со словарем. Без __init__ мы бы не знали, к какому
        именно полю относится валидатор, потому что __call__() вызывается с attrs - это весь словарь данных, и
        пришлось бы жёстко зашить "video_url" внутри валидатора, например так "value = attrs.get("video_url")".
        А это плохая практика потому что данный валидатор нельзя будет потом использовать для других полей (например,
        если в будущем появится trailer_url или teaser_url и тоже понадобится делать их валидацию на YouTube).
        """
        if isinstance(fields, str):
            self.fields = [fields]
        else:
            self.fields = list(fields)

    def __call__(self, attrs):
        """Метод __call__() делает экземпляр класса вызываемым, как функцию.
        Используется в DRF как валидатор поля сериализатора."""
        for field in self.fields:
            # Получаю поле из списка параметров, которое будем валидировать.
            validate_field = attrs.get(field)
            # Пропускаю пустые значения.
            if not validate_field:
                return
            # Задаю шаблон (регулярное выражение) для поиска всех вхождений URL (http:// или https://) в передаваемом
            # пользователе поле.
            url_pattern = re.compile(r"https?://[^\s]+")
            urls = url_pattern.findall(validate_field)
            for url in urls:
                # 1) Лучше не через оператор "IN" делать, а использовать urlparse из модуля urllib.parse, чтобы явно
                # получить домен из URL. Это надёжнее, чем просто искать подстроку "youtube.com" в полной ссылке, потому
                # что могут быть обманные случаи, например: "https://notyoutube.com/...", где "youtube.com" вроде бы
                # присутствует в строке, но на самом деле домен совсем другой. Если не извлекать домен отдельно, можно
                # случайно принять такую ссылку как допустимую.
                # 2) urlparse - парсит url на его составные части (scheme + netloc + path + params + query + fragment).
                parsed_url = urlparse(url)
                # 3) netloc - возвращает только имя домена, а не всю строку целиком.
                domain = parsed_url.netloc.lower()
                if domain not in self.allowed_domains:
                    raise serializers.ValidationError(
                        {field: "Разрешены только ссылки на YouTube (youtube.com)."}
                    )
