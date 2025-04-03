# LMS API (Django REST Framework)


[1. Цель проекта](#title1) / 
[2. Модели](#title2) / 
[3. Админки](#title3) / 
[4. Сериализации](#title4) / 
[5. Контроллеры](#title5) / 
[6. Вспомогательные функции](#title6) / 
[7. Загрузка тестовых данных](#title7) / 
[8. Установка проекта](#title8) / 
[9. Получение ключей .env](#title9) / 
[10. Описание файла .flake8](#title10) / 
[11. Описание файла mypy.ini](#title11) / 




# <a id="title1">1. Цель проекта</a>
Backend для разработки LMS-системы (онлайн-платформы обучения), в которой каждый желающий сможет размещать свои полезные материалы или курсы.
Разработка выполнена над SPA веб-приложением и результатом создания проекта будет бэкенд-сервер, который возвращает клиенту JSON-структуры.




# <a id="title2">2. Описание моделей (models)</a>

## _Приложение "Users" (users/models.py):_

1) Модель данных `CustomUser(AbstractUser)` - представляет Пользователя на платформе для онлайн-обучения (авторизация по email):
   - Наследуется от модели **AbstractUser**, которая является готовой моделью и включает все основные поля и методы, такие как username, email, first_name, last_name, is_staff, is_active и другие.
   - ***Дополнительно определил:***
     - ник пользователя (username);
     - эл.почта пользователя (email);
     - телефон пользователя (phone_number);
     - город пользователя (city);
     - аватар пользователя (avatar).

2) Модель данных `Payments(models.Model)`- представляет платежи за Lesson и/или за Course на платформе для онлайн-обучения:
   - пользователь (user).
   - дата и время оплаты (payment_date).
   - оплаченный курс (paid_course).
   - оплаченный урок (paid_lesson).
   - сумма платежа (payment_amount).
   - метод платежа (payment_method).

## _Приложение "lms_system" (lms_system/models.py):_

1) Модель данных `Course(models.Model)` - представляет Курс на платформе для онлайн-обучения:
   - название курса (title).
   - превью курса (preview).
   - описание курса (description).

2) Модель данных `Lesson(models.Model)` - представляет Урок на платформе для онлайн-обучения:
   - курс урока (course).
   - название урока (title).
   - описание урока (description).
   - превью урока (preview).
   - ссылка на видео урока (video_url).




# <a id="title3">3. Описание админок (admin)</a>

## _Приложение "Users" (users/admin.py):_

1) Админка `CustomUserAdmin(UserAdmin)` - отображение данный модели Пользователя (CustomUser) в админке.

## _Приложение "lms_system" (lms_system/admin.py):_

1) Админка `CourseAdmin(admin.ModelAdmin)` - отображение данных модели Курса (Course) в админке.

2) Админка `LessonAdmin(admin.ModelAdmin)` - отображение данных модели Урока (Lesson) в админке.




# <a id="title4">4. Описание сериализаций (serializers)</a>

## _Приложение "Users" (users/serializers.py):_

1) Сериализатор `CustomUserSerializer(serializers.ModelSerializer)` - класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на основе модели CustomUser. Описывает то, какие поля модели CustomUser будут участвовать в сериализации и десериализации.

## _Приложение "lms_system" (lms_system/serializers.py):_

1) Сериализатор `CourseSerializer(serializers.ModelSerializer)` - класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на основе модели Course. Описывает то, какие поля модели Course будут участвовать в сериализации и десериализации.
   - Кастомизация сериализатора:
     - функция `get_count_lessons()` - определение количества уроков в курсе (запрос в БД для подсчёта связанных уроков). Учитываю кастомный ***related_name="lessons"*** в модели Lesson.
     - поле `lessons_info` - с помощью сериализатора для связанной модели *Lesson* (**LessonSerializer()**) вывод детальной информации по всем урокам курса. 

2) Сериализатор `LessonSerializer(serializers.ModelSerializer)` - класс-сериализатор с использованием класса ModelSerializer для осуществления базовой сериализация в DRF на основе модели Lesson. Описывает то, какие поля модели Lesson будут участвовать в сериализации и десериализации.




# <a id="title5">5. Описание контроллеров (views)</a>

## _Приложение "Users" (users/views.py):_

1) Класс-контроллер `CustomUserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView)` - редактирование профилей любых пользователей.
   - на основе ***Generic*** - это компонент Django REST framework, который предоставляет набор готовых классов и миксинов для упрощения разработки RESTful API.

## _Приложение "lms_system" (lms_system/views.py):_

1) Класс-контроллер `CourseViewSet(viewsets.ModelViewSet)` - автоматический CRUD для модели Course.
   - на основе ***ModelViewSet*** - это компонент Django REST для эффективного управления API-ресурсами и уменьшения объема кода.
2) Класс-контроллер `LessonListCreateAPIView(generics.ListCreateAPIView)` - получение списка уроков и создание нового урока.
   - на основе ***Generic*** - это компонент Django REST framework, который предоставляет набор готовых классов и миксинов для упрощения разработки RESTful API.
3) Класс-контроллер `LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView)` - получение, обновление и удаление одного урока.
   - на основе ***Generic*** - это компонент Django REST framework, который предоставляет набор готовых классов и миксинов для упрощения разработки RESTful API.




# <a id="title6">6. Вспомогательные функции</a>

## _Приложение "Users" (users/managers.py):_

1) Класс `CustomUserManager(BaseUserManager)` - кастомный менеджер для пользователя без поля username:
   - функция `create_user()` - создает и возвращает обычного пользователя.
   - функция `create_superuser()` - создает и возвращает суперпользователя.




# <a id="title7">7. Загрузка тестовых данных</a>

## _Директория проекта для различных данных (data):_
1. Файл `courses.json` - тестовые данных для БД (таблица с данными курсов).
2. Файл `lessons.json` - тестовые данных для БД (таблица с данными уроков).
3. Файл `users.json` - тестовые данных для БД (таблица с данными пользователей).
4. Файл `payments.json` - тестовые данных для БД (таблица с данными платежей).

## _Приложение "lms_system" (lms_system/management/commands):_
1. `add_courses.py` - код кастомной команды по загрузке данных из `courses.json`.
2. `add_lessons.py` - код кастомной команды по загрузке данных из `lessons.json`.

## _Приложение "Users" (users/management/commands):_
1. `add_users.py` - код кастомной команды по загрузке данных из `users.json`.
2. `add_payments.py` - код кастомной команды по загрузке данных из `payments.json`.




# <a id="title8">8. Установка проекта</a>
1. Клонируйте репозиторий:
   ```
   git clone https://github.com/MaksimLakovich/Homework-5-python-DJANGO-REST-FRAMEWORK.git
   ```
2. Установите зависимости:
   ```
   poetry install
   ```
3. Заполните файл `.env` по примеру `.env.example`




# <a id="title9">9. Получение ключей. Описание файла .env.example</a> 
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




# <a id="title10">10. Описание файла .flake8</a> 
```angelscript
[flake8]
max-line-length = 119
ignore = E203, W503
exclude = .git, __pycache__, venv, .venv
```




# <a id="title11">11. Описание файла mypy.ini</a> 
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