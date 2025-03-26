# LMS API (Django REST Framework)


[1. Цель проекта](#title1) / 
[2. Модели](#title2) /
[9. Установка проекта](#title9) / 
[10. Получение ключей](#title10) /




# <a id="title1">1. Цель проекта</a>
Backend для разработки LMS-системы (онлайн-платформы обучения), в которой каждый желающий сможет размещать свои полезные материалы или курсы.
Разработка выполнена над SPA веб-приложением и результатом создания проекта будет бэкенд-сервер, который возвращает клиенту JSON-структуры.




# <a id="title2">2. Описание моделей (models)</a>

## _Приложение "lms_system" (lms_system/models.py):_

1) Реализация модели ***Category***, которая представляет категорию товаров в интернет-магазине:
   - наименование (category_name);
   - описание (description).

## _Приложение "Users" (users/models.py):_

1) Реализация модели ***UserCustomer(AbstractUser)***, которая представляет пользователя магазина:
   - Включает все основные поля и методы, такие как username, email, first_name, last_name, is_staff, is_active и другие.
   - `Дополнительно определил:`
     - почта пользователя (email);
     - аватар пользователя (avatar);
     - телефон пользователя (phone_number);
     - страна пользователя (country);
     - имя пользователя (first_name);
     - фамилия пользователя (last_name).
   - `Модель UserCustomer(AbstractUser) дополнительно использует кастомный менеджер UserCustomerManager() из "users/managers.py":`
     - ***class UserCustomerManager(BaseUserManager)*** - кастомный менеджер для пользователя без поля username.:
       - метод **def create_user()**: создает и возвращает обычного пользователя;
       - метод **def create_superuser()**: создает и возвращает суперпользователя (админа).




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
   - Настройки секретного ключа проекта:
     - SECRET_KEY_FOR_PROJECT = *secret_key_here*
   - Настройки дебага (обратить внимание, что в settings.py дебаг дополнительно должен быть описан так: DEBUG = True if os.getenv('DEBUG') == 'True' else False):
     - DEBUG = True
   - Настройки БД:
     - DATABASE_NAME = *write_here*
     - DATABASE_USER = *write_here*
     - DATABASE_PASSWORD = *write_here*
     - DATABASE_HOST = *write_here*
     - DATABASE_PORT = *write_here*
