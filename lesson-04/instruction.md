# Lesson 04 — Postgres + модели + миграции

## Что сделано
В существующем Django-проекте `2026-MAI-Backend-I-Lyapin/project/` расширена схема БД так, чтобы были связи:
- **ForeignKey**: `Movie.genre -> Genre`
- **ManyToMany**: `Movie.actors <-> Actor`, `Movie.favorited_by <-> auth.User`
- **OneToOne**: `UserProfile.user -> auth.User`

Также добавлено поле `Movie.description` (оно понадобится для поиска в ДЗ №5).

## Требования из задания (чеклист)
- [x] Postgres: установить, создать пользователя/БД, настроить доступ
- [x] Спроектировать модели и применить миграции в БД
- [x] Должны присутствовать связи **OneToOne**, **ForeignKey**, **ManyToMany**

## Где лежит код
- `project/movies/models.py` — модели `Actor`, `UserProfile`, новые поля в `Movie`
- `project/movies/migrations/0008_*.py` — миграция с новыми сущностями/полями
- `project/movies/migrations/0009_*.py` — миграция с правкой `Movie.added_at`
- `project/project/settings.py` — конфигурация БД через переменные окружения (+ флаг SQLite)

## Настройка Postgres (пример)
Создай пользователя и БД (примерные команды, можно через pgAdmin):

```sql
CREATE USER quack_user_2023 WITH PASSWORD 's3cr3t';
CREATE DATABASE quack_db_2023 OWNER quack_user_2023;
GRANT ALL PRIVILEGES ON DATABASE quack_db_2023 TO quack_user_2023;
```

## Проверка подключения к Postgres
Убедись, что можешь подключиться (пример):
- Host: `127.0.0.1`
- Port: `5432`
- DB: `quack_db_2023`
- User: `quack_user_2023`
- Password: `s3cr3t`

## Как подключить Postgres к проекту
По умолчанию проект настроен на Postgres и читает параметры из env:
- `DB_NAME` (default: `quack_db_2023`)
- `DB_USER` (default: `quack_user_2023`)
- `DB_PASSWORD` (default: `s3cr3t`)
- `DB_HOST` (default: `127.0.0.1`)
- `DB_PORT` (default: `5432`)

Пример для PowerShell (если хочешь задать явно):

```bash
$env:DB_NAME="quack_db_2023"
$env:DB_USER="quack_user_2023"
$env:DB_PASSWORD="s3cr3t"
$env:DB_HOST="127.0.0.1"
$env:DB_PORT="5432"
```

## Применить миграции в Postgres
Из корня репозитория:

```bash
python 2026-MAI-Backend-I-Lyapin/project/manage.py migrate
```

## Локальный запуск без Postgres (SQLite)
Чтобы можно было проверять код без поднятого Postgres, добавлен переключатель:
- если `USE_SQLITE=1`, используется SQLite `db.sqlite3` в папке `project/`.

Пример (PowerShell):

```bash
$env:USE_SQLITE="1"
python 2026-MAI-Backend-I-Lyapin/project/manage.py migrate
```

## Частые проблемы
- `psycopg2` не ставится → на Windows чаще всего помогает установка через `pip` (в этой среде уже ставится), либо установка build tools.
- `FATAL: password authentication failed` → проверь пароль/пользователя и `pg_hba.conf`.

