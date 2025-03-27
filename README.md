# LMS API (Django REST Framework)


[1. Цель проекта](#title1) / 
[2. Модели](#title2) / 
[3. Админки](#title3) / 
[9. Установка проекта](#title9) / 
[10. Получение ключей .env](#title10) / 
[11. Описание файла .flake8](#title11) / 
[12. Описание файла mypy.ini](#title12) / 




# <a id="title1">1. Цель проекта</a>
Backend для разработки LMS-системы (онлайн-платформы обучения), в которой каждый желающий сможет размещать свои полезные материалы или курсы.
Разработка выполнена над SPA веб-приложением и результатом создания проекта будет бэкенд-сервер, который возвращает клиенту JSON-структуры.




# <a id="title2">2. Описание моделей (models)</a>

## _Приложение "Users" (users/models.py):_

1) Модель данных `CustomUser(AbstractUser)` - представляет пользователя на платформе для онлайн-обучения:
   - Наследуется от модели **AbstractUser**, которая является готовой моделью и включает все основные поля и методы, такие как username, email, first_name, last_name, is_staff, is_active и другие.
   - ***Дополнительно определил:***
     - ник пользователя (username);
     - эл.почта пользователя (email);
     - телефон пользователя (phone_number);
     - город пользователя (city);
     - аватар пользователя (avatar).

## _Приложение "lms_system" (lms_system/models.py):_

1) ...




# <a id="title3">3. Описание админок (admin)</a>

## _Приложение "Users" (users/admin.py):_

1) Админка `CustomUserAdmin(UserAdmin)` - отображение модели пользователя (CustomUser) в админке.

## _Приложение "lms_system" (lms_system/admin.py):_

1) ...




# <a id="title9">9. Установка проекта</a>
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/MaksimLakovich/Homework-5-python-DJANGO-REST-FRAMEWORK.git
   ```
2. Установите зависимости:
   ```
   poetry install
   ```
3. Заполните файл `.env` по примеру `.env.example`




# <a id="title10">10. Получение ключей. Описание файла .env.example</a> 
1. Создайте файл .env в корне проекта из копии подготовленного файла `.env.example`, в котором описаны названия всех переменных, необходимых для работы приложения.
2. Замените значения переменных реальными данными.
3. В модуле `settings.py` существует секретный ключ `SECRET_KEY`, который рекомендуется в целях безопасности хранить в тайне:
4. Файл .env должен содержать данные:
```dotenv
# Настройки секретного ключа проекта django в config/settings.py
#Django рекомендует в целях безопасности хранить секретный ключ, используемый в продакшене, в тайне!
SECRET_KEY_FOR_PROJECT=secret_key_here

# Настройки дебага.
# В settings.py дебаг должен быть описан так: DEBUG = True if os.getenv('DEBUG') == 'True' else False
DEBUG=

# Настройки БД проекта django в config/settings.py
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```




# <a id="title11">11. Описание файла .flake8</a> 
```angelscript
[flake8]
max-line-length = 119
ignore = E203, W503
exclude = .git, __pycache__, venv, .venv
```




# <a id="title12">12. Описание файла mypy.ini</a> 
```ini
# Настроил mypy для Django, указав путь к settings.py.
# Это нужно было чтоб убрать ошибки проверки mypy
# из-за того, что он не распознавал phonenumber_field,
# так как у phonenumber_field нет type stubs.
[mypy]
plugins = mypy_django_plugin.main

# Указываем настройки для плагина Django.
[mypy.plugins.django-stubs]
django_settings_module = config.settings

# Пробовал игнорировать phonenumber_field в mypy.ini,
# но это не сработало, и поэтому пришлось добавить
# в код (users/models.py) вот это "# type: ignore"
# на импорт PhoneNumberField, и ошибка исчезла.
[mypy-phonenumber_field.*]
ignore_missing_imports = True
```