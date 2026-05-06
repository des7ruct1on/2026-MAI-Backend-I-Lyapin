## ДЗ‑3 (Django + nginx)

### Цель

Собрать минимальный Django‑проект и подготовить два набора эндпоинтов:

- `/web/` — “веб‑часть” (HTML), чтобы что‑то отображалось в браузере
- `/api/` — “данные” (JSON), заглушки для будущего SPA/клиента

### Что нужно было сделать

- Создать и запустить Django‑проект
- Сделать заглушки API на `JsonResponse` (профиль, список продуктов, страница категории и т.д.)
- В `nginx.conf` сделать 2 `location` (`/web/` и `/api/`), которые ходят в Django
- Обрабатывать только нужные методы (GET/POST)

## ДЗ‑4 (PostgreSQL + модели + миграции)

### Цель

Подключить PostgreSQL к проекту и перенести структуру данных в БД через Django ORM и миграции.

### Что нужно было сделать

- Установить PostgreSQL, создать пользователя и БД, настроить доступ
- Спроектировать модели, чтобы была минимум одна связь из списка:
  - OneToOne / ForeignKey / ManyToMany
- Создать и применить миграции в PostgreSQL

## Структура решения (файлы и ответственность)

### Папки/файлы проекта

- `lesson-03/homework.md`
  - **Зачем**: постановка ДЗ‑3
  - **Кем создан**: дано в репозитории (не генерируется)

- `lesson-04/homework.md`
  - **Зачем**: постановка ДЗ‑4
  - **Кем создан**: дано в репозитории (не генерируется)

- `lesson-03/nginx.conf`
  - **Зачем**: nginx проксирует `/web/` и `/api/` на Django upstream `127.0.0.1:8001`
  - **Кем создан**: дано в репозитории (не генерируется)

- `lesson-03/uniapp/`
  - **Зачем**: корень Django‑проекта (запуск через `manage.py`)
  - **Кем создан**: создан командой `django-admin startproject` (генерируется), дальше дополнялся вручную

- `lesson-03/uniapp/manage.py`
  - **Зачем**: CLI‑точка управления Django (`runserver`, `migrate`, `makemigrations`, `test`)
  - **Кем создан**: генерируется Django

- `lesson-03/uniapp/uniapp/settings.py`
  - **Зачем**: настройки Django; переключение SQLite/PostgreSQL сделано через env‑переменные `POSTGRES_*`
  - **Кем создан**: генерируется Django, затем редактировался вручную

- `lesson-03/uniapp/uniapp/urls.py`
  - **Зачем**: роутинг верхнего уровня; подключает `main.web_urls` и `main.api_urls`
  - **Кем создан**: генерируется Django, затем редактировался вручную

- `lesson-03/uniapp/main/`
  - **Зачем**: Django‑приложение, где лежат заглушки и модели
  - **Кем создан**: создано командой `manage.py startapp` (генерируется), затем дополнялось вручную

- `lesson-03/uniapp/main/views.py`
  - **Зачем**: заглушки `/web/` и `/api/*` + ограничение методов через `require_http_methods`
  - **Кем создан**: редактировался вручную

- `lesson-03/uniapp/main/web_urls.py`
  - **Зачем**: маршруты веб‑части (`/web/`)
  - **Кем создан**: написан вручную

- `lesson-03/uniapp/main/api_urls.py`
  - **Зачем**: маршруты API‑части (`/api/`)
  - **Кем создан**: написан вручную

- `lesson-03/uniapp/main/templates/main/index.html`
  - **Зачем**: HTML для `/web/`
  - **Кем создан**: написан вручную

- `lesson-03/uniapp/main/models.py`
  - **Зачем**: модели для ДЗ‑4 (есть связи `ForeignKey` и `ManyToMany`)
  - **Кем создан**: редактировался вручную

- `lesson-03/uniapp/main/migrations/0001_initial.py`
  - **Зачем**: миграция, создаёт таблицы моделей `main`
  - **Кем создан**: генерируется автоматически командой `makemigrations`

- `requirements.txt`
  - **Зачем**: зависимости (в т.ч. `psycopg` для PostgreSQL)
  - **Кем создан**: формируется командой `pip freeze` (генерируется)

## Запуск ДЗ‑3 (быстрый запуск на SQLite)

Команды выполняй из корня репозитория.

### 1) Установка зависимостей

```bash
python -m venv venv
./venv/bin/python -m pip install -r requirements.txt
```

### 2) Миграции

```bash
./venv/bin/python lesson-03/uniapp/manage.py migrate
```

### 3) Запуск Django

```bash
./venv/bin/python lesson-03/uniapp/manage.py runserver 127.0.0.1:8001
```

### 4) Проверка в браузере

- `http://127.0.0.1:8001/web/`
- `http://127.0.0.1:8001/api/profile/` (GET)
- `http://127.0.0.1:8001/api/products/` (GET)
- `http://127.0.0.1:8001/api/category/1/` (GET)

POST‑ручка:

- `http://127.0.0.1:8001/api/favorites/add/` (POST)

Пример проверки через curl:

```bash
curl -X POST http://127.0.0.1:8001/api/favorites/add/
```

Если сделать запрос неправильным методом (например POST на `/api/profile/`), Django вернёт `405 Method Not Allowed`.

## Запуск ДЗ‑3 через nginx (опционально)

В `lesson-03/nginx.conf` upstream ждёт Django на `127.0.0.1:8001`, поэтому порядок такой:

1) запусти Django как выше
2) запусти nginx с этим конфигом (способ зависит от того, как установлен nginx в системе)

После этого запросы на nginx будут проксироваться на Django:

- `/web/` → Django
- `/api/` → Django

## Запуск ДЗ‑4 (PostgreSQL)

### 1) Установить и запустить PostgreSQL

Способ установки зависит от системы (brew / Postgres.app / docker). Главное — чтобы сервер слушал `127.0.0.1:5432`.

### 2) Создать пользователя и БД

Пример SQL (в psql под админом):

```sql
CREATE USER uniapp_user WITH PASSWORD 'uniapp_pass';
CREATE DATABASE uniapp_db OWNER uniapp_user;
```

### 3) Экспортировать переменные окружения

Если `POSTGRES_DB` не задана — проект использует SQLite.

```bash
export POSTGRES_DB="uniapp_db"
export POSTGRES_USER="uniapp_user"
export POSTGRES_PASSWORD="uniapp_pass"
export POSTGRES_HOST="127.0.0.1"
export POSTGRES_PORT="5432"
```

### 4) Применить миграции в PostgreSQL

```bash
./venv/bin/python lesson-03/uniapp/manage.py migrate
```

### 5) Проверить, что таблицы реально в PostgreSQL

```bash
psql --host=127.0.0.1 --port=5432 --user=uniapp_user --dbname=uniapp_db -c "\dt"
```

Ожидаемые таблицы (минимум):

- `main_category`
- `main_product`
- `main_profile`
- `main_profile_favorites`

### 6) Запуск сервера (уже на PostgreSQL)

```bash
./venv/bin/python lesson-03/uniapp/manage.py runserver 127.0.0.1:8001
```

## Частые проблемы

- Если в `psql` видишь приглашение вида `postgres-#`, это означает незаконченный ввод (например, ты ввёл команду без `;` или начал строку в кавычках).
  - Нажми `Ctrl+C` чтобы сбросить ввод
  - Либо введи `\r`
  - Выйти: `\q`

- Если `\dt` в `uniapp_db` пишет `Did not find any relations`, значит миграции в PostgreSQL не применялись или ты не в той БД.
  - Проверь подключение именно к `--dbname=uniapp_db`
  - Проверь, что `POSTGRES_DB` экспортирована в том же терминале, где запускаешь `manage.py migrate`

