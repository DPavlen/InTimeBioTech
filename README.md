# InTimeBioTech

## 1. [Задание и требования](#1)
## 2. [Функционал API, эндпойнты и технические особенности](#2)
## 3. [Стек технологий](#3)
## 4. [Запуск проекта через docker compose и ссыылка на него](#4)
## 5. [Автор проекта:](#5)

## 1. Описание  <a id=1></a>
1. Настройка проекта и контроль версий:
    - Создайте новый проект Django и настройте виртуальную среду.
    — Инициализируйте репозиторий Git для контроля версий.

2. **Проектирование и реализация API:**
    - Разработка конечных точек RESTful API для регистрации пользователей, входа в систему, получения профиля пользователя, обновления профиля пользователя и удаления учетной записи с помощью Django Rest Framework (DRF).
    - Реализуйте конечные точки с помощью соответствующих функций просмотра и сериализаторов.

3. **Безопасное хеширование и хранение паролей:**
    - Внедрить безопасное хеширование и хранение паролей с использованием алгоритма хеширования Django (например, Argon).
    - Убедитесь, что простые пароли не хранятся в базе данных.

4. **Проверка, обработка ошибок и документация:**
    - Применяйте соответствующие методы проверки и обработки ошибок для конечных точек API.
    - Документируйте конечные точки API, форматы запросов/ответов и обработку ошибок.

5. **Пользовательская модель пользователя и аутентификация:**
    - Создайте собственную модель пользователя, включающую электронную почту в качестве уникального идентификатора.
    - Внедрить механизмы аутентификации и авторизации на основе электронной почты для защиты маршрутов API.

6. **Очередь сообщений с Celery:**
    - Интегрируйте Celery для отправки OTP пользователям во время входа в систему.
    - Отправьте 6-значные OTP-коды на электронные письма пользователей и подтвердите их для входа. Реализуйте срок действия OTP.

7. **База данных и развертывание:**
    - Выберите базу данных по вашему выбору (например, PostgreSQL).
    - Настройка моделей баз данных для хранения профилей пользователей и других соответствующих данных.
- Документируйте, как настроить и развернуть серверное приложение.



## 2. Функционал API, эндпойнты и технические особенности <a id=2></a>
- https://localhost/api/swagger/ реализована возможность автоматической генерации документации для вашего API, с помощью Swagger
- https://localhost/api/redoc/ реализована возможность автоматической генерации документации для вашего API, с помощью Redoc
- http://localhost/api/v1/users/  Djoser эндпойнты. Работа с пользователями. Регистрация пользователей, удаление, изменение данных.Вывод пользователей. POST, GET, PUT, PATCH, DEL запросы.(Смотри документацию Swagger или Redoc)
- http://localhost/api/v1/users/verification_code/ POST-запрос. Кастомный эндпйонт для создания кода верификации. Соответсвенно с помощью  Celery и Redis для отправки задач в фоновом режиме настроена отправка уведомления на почту с OTP CODE.
- http://localhost/api/v1/users/auth_otp_code/  POST-запрос. Кастомный эндпйонт для проверки OTP-кода и аутентификации пользователя. И пользователь успешно получил Auth_Token.
- http://localhost/api/v1/auth/token/login/ Djoser эндпойнт.POST-запрос. Вход по логину и паролю и получение токена.
- http://localhost/api/v1/auth/token/login/ Djoser эндпойнт.POST-запрос. Выход и удаление токена.

Пример функционала
[text](<../../Projects/InTimeBioTech/Отчет о тестировании/Функционал проекта.odt>)

## 3. Стек технологий <a id=3></a>
[![Django](https://img.shields.io/badge/Django-4.2.1-6495ED)](https://www.djangoproject.com) [![Djangorestframework](https://img.shields.io/badge/djangorestframework-3.14.0-6495ED)](https://www.django-rest-framework.org/) [![Django Authentication with Djoser](https://img.shields.io/badge/Django_Authentication_with_Djoser-2.2.0-6495ED)](https://djoser.readthedocs.io/en/latest/getting_started.html) [![Nginx](https://img.shields.io/badge/Nginx-1.21.3-green)](https://nginx.org/ru/)  [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/) [![Celery](https://img.shields.io/badge/Celery-%205.2.7-blue?style=flat-square&logo=celery)](https://docs.celeryq.dev/en/stable/)[![Redis](https://img.shields.io/badge/Redis-%205.0.0-blue?style=flat-square&logo=redis)](https://redis.io/) [![Swagger](https://img.shields.io/badge/Swagger-%201.21.7-blue?style=flat-square&logo=swagger)](https://swagger.io/) [![Gunicorn](https://img.shields.io/badge/Gunicorn-%2020.0.4-blue?style=flat-square&logo=gunicorn)](https://gunicorn.org/) [![Docker](https://img.shields.io/badge/Docker-%2024.0.5-blue?style=flat-square&logo=docker)](https://www.docker.com/) [![DockerCompose](https://img.shields.io/badge/Docker_Compose-%202.21.0-blue?style=flat-square&logo=docsdotrs)](https://docs.docker.com/compose/)

## 4. Запуск проекта через docker compose и ссыылка на него <a id=4></a>

## Запуск проекта локально в Docker-контейнерах с помощью Docker Compose

Склонируйте проект из репозитория:

```shell
git clone https://github.com/DPavlen/InTimeBioTech.git
```


Перейдите в директорию проекта:

```shell
cd backend_Django/
```

Перейдите в директорию **docker** и создайте файл **.env**:

```shell
cd docker/
```

```shell
nano .env
```

Добавьте строки, содержащиеся в файле **.env.example** и подставьте 
свои значения.

Пример из .env файла:

```dotenv
SECRET_KEY=DJANGO_SECRET_KEY        # Ваш секретный ключ Django
DEBUG=False                         # True - включить Дебаг. Или оставьте пустым для False
IS_LOGGING=False                    # True - включить Логирование. Или оставьте пустым для False
ALLOWED_HOSTS=127.0.0.1 backend     # Список адресов, разделенных пробелами


# Помните, если вы выставляете DEBUG=False, то необходимо будет настроить список ALLOWED_HOSTS.
# 127.0.0.1 и backend является стандартным значением. Через пробел.
# Присутствие backend в ALLOWED_HOSTS обязательно. Через название сервиса :
# docker-compose осуществляется отправка почтовых писем.

DB_ENGINE=postgresql

POSTGRES_USER=django_user                  # Ваше имя пользователя для бд
POSTGRES_PASSWORD=django                   # Ваш пароль для бд
POSTGRES_DB=django                         # Название вашей бд
DB_HOST=db                                 # Стандартное значение - db
DB_PORT=5432                               # Стандартное значение - 5432

EMAIL_HOST=smtp.yandex.ru                  # Адрес хоста эл. почты
EMAIL_PORT=465                             # Порт эл. почты
EMAIL_USE_TLS=True/False                   # Использование TLS
EMAIL_USE_SSL=True/False                   # Использование SSL
EMAIL_HOST_USER=info@prosept.ru            # Адрес почты, с которой будут отправляться письма
EMAIL_HOST_PASSWORD=SecretPassword         # Пароль почты, с которой будут отправляться письма
DEFAULT_FROM_EMAIL=info@prosept.ru         # Адрес почты, с которой будут отправляться письма
```

```shell
В директории **docker** проекта находится файл **docker-compose.local.yaml**, с 
помощью которого вы можете запустить проект локально в Docker контейнерах.
```

Находясь в директории **docker** выполните следующую команду:

> **Примечание.** Если нужно - добавьте в конец команды флаг **-d** для запуска
> в фоновом режиме.

```shell
sudo docker compose -f docker-compose.local.yaml up
```
Она сбилдит Docker образы и запустит backend, frontend, СУБД, Celery, Redis 
и Nginx в отдельных Docker контейнерах.

По завершении всех операции проект будет запущен и доступен по адресу
http://127.0.0.1/ или http://localhost/ в зависимости от настроек

Для остановки Docker контейнеров, находясь в директории **docker** выполните 
следующую команду:

```shell
sudo docker compose -f docker-compose.yml down
```

Либо просто завершите работу Docker Compose в терминале, в котором вы его
запускали, сочетанием клавиш **CTRL+C**.

***
 
## 5. Автор проекта: <a id=5></a> 

**Павленко Дмитрий**  
- Ссылка на мой профиль в GitHub [Dmitry Pavlenko](https://github.com/DPavlen)  
