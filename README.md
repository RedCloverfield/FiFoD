# Проект для работы с файлами FiFoD

Проект FiFoD — это прототип сервиса для управления файлами, привязанными к устройствам, получаемым с внешнего API.
Ключевые возможности сервиса:

* загрузка файлов на сервер;
* получение списка файлов (с расширениями '.jpg', '.png', '.gif', 'jpeg', 'bmp'), загруженных на сервер;
* получение списка доступных и готовых к использованию устройств с внешнего API;
* создание привязок между файлами на сервере и устройствами;
* просмотр созданных привязок;
* получение статуса фоновых задач, запущенных при создании привязок.

Пользовательский интерфейс сервиса — Swagger документация, позволяющая осуществлять все вышеуказанные операции. Для осуществления операций необходимо зарегистрироваться в системе, воспользовавшись эндпоинтом */users/register-user* и указав учетные данные. После этого необходимо пройти аутентификацию с использованием тех же учетных данных.

## Стэк используемых технологий
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-%23D71F00.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Pydantic](https://img.shields.io/badge/pydantic-%23E92063.svg?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/latest/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4)](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
[Alembic](https://alembic.sqlalchemy.org/)
[Uvicorn](https://uvicorn.dev/)

## Разворачивание проекта в Docker-сети

> [!NOTE]
> Перед началом работы убедитесь, что на машине, на которой производится запуск данного проекта установлен Docker.

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/RedCloverfield/FiFoD.git
```

```
cd FiFoD
```
2. Создать файл .env со структурой подобной структуре файла .env.example.

> [!WARNING]
> ОБРАТИТЕ ВНИМАНИЕ! Для создания пользователей необходимо обладать правами администратора. Для данной цели при инициализации проекта создается суперпользователь с учетными данными, которые будут указаны в переменных `SUPERUSER_NAME` (имя пользователя) и `SUPERUSER_PASSWORD` (пароль пользователя).

> [!WARNING]
> ОБРАТИТЕ ВНИМАНИЕ! Перед началом работы с проектом необходимо создать директорию, для хранения файлов, путь к которой затем следует указать в переменной `FILES_STORAGE_DIR`.

```
#JWT settings
SECRET_KEY - секретный ключ проекта
ALGORITHM - алгоритм шифрования ключа
ACCESS_TOKEN_EXPIRE_MINUTES - срок действия JWT Access токена в минутах
REFRESH_TOKEN_EXPIRE_MINUTES - срок действия JWT Refresh токена в минутах

# External API settings
EXTERNAL_API_TOKEN - Bearer токен внешнего API для получения списка устройств
EXTERNAL_API_URL - URL внешнего API

# Posgres settings
POSTGRES_PASSWORD - пароль базы данных PostgreSQL
POSTGRES_USER - имя пользователя базы данных PostgreSQL
POSTGRES_DB - название базы данных PostgreSQL
POSTGRES_HOSTNAME - хост, на котором развернута база данных PostgreSQL (должен соответствовать названию контейнера в Docker сети)

# Superuser settings
SUPERUSER_NAME - никнейм первого суперпользователя
SUPERUSER_PASSWORD - пароль первого суперпользователя

# Redis settings
REDIS_USER - имя пользователя базы данных Redis
REDIS_PASSWORD - пароль базы данных Redis
REDIS_HOSTNAME - хост, на котором развернута база данных Redis (должен соответствовать названию контейнера в Docker сети)
REDIS_DB_BROKER - номерное название базы базы данных Redis, выступающей брокером сообщений для Celery
REDIS_DB_RESULT - номерное название базы базы данных Redis, выступающей бэкендом для Celery

# Files settings
FILES_STORAGE_DIR - директория для хранения файлов на сервере (если на момент запуска сервиса директория не существует, ее необходимо создать вручную)
```
3. Запустить контейнеризацию приложения через docker compose

```
sudo docker compose up --build
````

Если все шаги проделаны правильно, приложение станет доступно по URL: http://localhost:8000/api/v1/docs.
Для остановки приложение и всех Docker контейнеров воспользуйтесь терминальной командой

```
sudo docker compose down
````

## Автор проекта
[Ефимов Станислав](https://github.com/RedCloverfield)