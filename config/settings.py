import os
import sys
from datetime import timedelta
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

# Загрузка переменных из .env-файла
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY_FOR_PROJECT')

DEBUG = True if os.getenv('DEBUG') == 'True' else False

# ALLOWED_HOSTS в Django - это список доменов/IP, с которых разрешено обращаться к приложению.
# 1) Если поставить ['*'], то Django будет принимать запросы с любого домена/IP. Это удобно на этапе тестового
# деплоя (ВМ, Nginx), когда ещё нет точного домена.
# 2) Но в боевой среде так оставлять не рекомендуется - лучше явно указать:
# ALLOWED_HOSTS = ["mydomain.com", "www.mydomain.com", "123.45.67.89"]
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Добавляем это чтобы библиотека https://django-phonenumber-field.readthedocs.io/en/stable/index.html
    # использовала локализованные ошибки валидации номеров в поле PhoneNumberField
    'phonenumber_field',
    # DRF (Django REST framework) - это библиотека, которая работает со стандартными моделями Django для создания
    # гибкого и мощного API-сервера для проекта.
    'rest_framework',
    # Для использования расширенной фильтрации с помощью пакета django-filter, после его установки
    'django_filters',
    # Если будем использовать Localizations/translations, то нужно добавить REST_FRAMEWORD_SIMPLEJWT в INSTALLED_APPS
    'rest_framework_simplejwt',
    # Добавляем drf_yasg для работы с Документацией DRF
    'drf_yasg',
    # Приложения проекта
    'users',
    'lms_system',
    # Добавляем celery beat для работы с периодическими задачами
    'django_celery_beat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT', default='5432'),
    }
}

# База данных для тестов при разворачивании приложения (чтоб не разворачивать сразу postgresql достаточно в начале
# для тестов развернуть sqlite
if 'test' in sys.argv:
    # это чтоб выполнять задачи синхронно, без брокера. Чтоб в GitHub Actions не появлялась ошибка при деплое
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# STATIC_ROOT важен при развертывании приложения на ВМ и использовании Nginx
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=180),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

SECRET_KEY_FOR_STRIPE = os.getenv('SECRET_KEY_FOR_STRIPE')

# Настройки для Celery
# URL-адрес брокера сообщений. Например, Redis, который по умолчанию работает на порту 6379 — адрес брокера сообщений.
# Формат: redis://<host>:<port>/<db_number>.
# /0 и /1 и так далее — разные базы в Redis (например, чтобы задачи Celery и кэш Django не мешали друг другу).
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')

# URL-адрес брокера результатов — хранилище результатов выполнения задач. Можно использовать тот же Redis,
# что и для брокера.
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')

# Часовой пояс для работы Celery — важно для периодических задач, чтобы они выполнялись в правильное время.
# Пример, CELERY_TIMEZONE = "Australia/Tasmania", я ссылаюсь на наш TIME_ZONE проекта, чтоб все было в одном поясе
CELERY_TIMEZONE = TIME_ZONE

# Флаг отслеживания выполнения задач — Celery будет отслеживать состояние "в процессе".
CELERY_TASK_TRACK_STARTED = True

# Максимальное время на выполнение задачи
CELERY_TASK_TIME_LIMIT = 30 * 60

# Подключение почтового сервера в Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('YANDEX_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('YANDEX_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Настройки для Celery по запуску периодических задач
CELERY_BEAT_SCHEDULE = {
    'task-deactivate-inactive-users-every-day': {
        'task': 'users.tasks.task_deactivate_inactive_users',
        # 'schedule': timedelta(minutes=3),  # Расписание выполнения задачи (например, каждые 3 минут)
        'schedule': crontab(hour=0, minute=0),  # Каждый день в полночь
    },
}
