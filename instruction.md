## Что сделано

- **ДЗ-3**: создан Django-проект в `lesson-03/uniapp/`
- **ДЗ-3**: добавлены заглушки для `/api/*` на `JsonResponse` и страница `/web/`
- **ДЗ-3**: ограничены методы на ручках через `require_http_methods`
- **ДЗ-3**: подготовлен `lesson-03/nginx.conf` с location `/web/` и `/api/` на upstream Django
- **ДЗ-4**: добавлены модели и миграции для БД (есть `ForeignKey` и `ManyToMany`)
- **ДЗ-4**: добавлена поддержка PostgreSQL через переменные окружения (если они заданы, используется Postgres, иначе SQLite)

## Структура

- `lesson-03/uniapp/` — Django-проект
- `lesson-03/nginx.conf` — конфиг nginx для проксирования `/web/` и `/api/`
- `lesson-04/homework.md` — постановка ДЗ-4 (реализация сделана в Django-проекте из `lesson-03`)

## Запуск с нуля

### Вариант 1. SQLite (быстрый запуск)

```bash
python -m venv venv
./venv/bin/python -m pip install -r requirements.txt
./venv/bin/python lesson-03/uniapp/manage.py migrate
./venv/bin/python lesson-03/uniapp/manage.py runserver 127.0.0.1:8001
```

Проверка в браузере:

- `http://127.0.0.1:8001/web/`
- `http://127.0.0.1:8001/api/profile/`
- `http://127.0.0.1:8001/api/products/`
- `http://127.0.0.1:8001/api/category/1/`

### Вариант 2. PostgreSQL (под ДЗ-4)

1) Установить PostgreSQL.

2) Создать пользователя и БД (пример):

```sql
CREATE USER uniapp_user WITH PASSWORD 'uniapp_pass';
CREATE DATABASE uniapp_db OWNER uniapp_user;
```

3) Запуск с переменными окружения:

```bash
export POSTGRES_DB="uniapp_db"
export POSTGRES_USER="uniapp_user"
export POSTGRES_PASSWORD="uniapp_pass"
export POSTGRES_HOST="127.0.0.1"
export POSTGRES_PORT="5432"

./venv/bin/python lesson-03/uniapp/manage.py migrate
./venv/bin/python lesson-03/uniapp/manage.py runserver 127.0.0.1:8001
```

## Nginx

В `lesson-03/nginx.conf` уже настроены location:

- `/web/` → Django upstream
- `/api/` → Django upstream

Upstream ожидает Django на `127.0.0.1:8001`.

## Тестирование (что запускалось)

```bash
./venv/bin/python lesson-03/uniapp/manage.py migrate
./venv/bin/python lesson-03/uniapp/manage.py test
```

Результат:

- миграции применились успешно
- тесты: `NO TESTS RAN` (в проекте тесты не добавлялись)

