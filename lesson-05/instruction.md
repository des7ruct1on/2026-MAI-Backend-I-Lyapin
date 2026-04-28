# Lesson 05 — реальные вьюхи (search/list/create)

## Что сделано
Заглушки API из ДЗ №3 заменены на реальные вьюхи, которые работают с БД (модель `Movie`).

Реализовано:
- `GET /api/search/?q=...` — поиск фильмов по двум полям: `title` и `description`
- `GET /api/movies/` — получение всех фильмов из БД
- `POST /api/movies/create` — создание фильма в БД

Все ответы — `JsonResponse`, методы ограничены `@require_http_methods`.

## Требования из задания (чеклист)
- [x] `GET /search?q=...` возвращает JsonResponse и ищет минимум по 2 полям
- [x] `GET /<plural>/` возвращает JsonResponse и принимает **только GET**
- [x] `POST /<plural>/create` возвращает JsonResponse и принимает **только POST**

## Где лежит код
- `project/movies/api_views.py` — `search`, `movies_feed`, `movies_create`
- `project/movies/api_urls.py` — роуты `/api/...`

## Эндпоинты (как их дергать)
### Поиск
- `GET /api/search/?q=silence`

Ищет по:
- `Movie.title` (icontains)
- `Movie.description` (icontains)

### Получить все фильмы
- `GET /api/movies/`

### Создать фильм
- `POST /api/movies/create`

## Формат POST /api/movies/create
Тело запроса (JSON):

```json
{
  "title": "Movie title",
  "description": "Some description",
  "year": 2026,
  "genre_id": 1
}
```

- `title` — обязателен
- `genre_id` — опционален (если указан, должен существовать)

## Локальная проверка на SQLite
Есть автотест, который:
- поднимает Django (SQLite)
- создаёт тестовые жанры/фильмы
- проверяет `search`, `movies`, `create`

Запуск из корня:

```bash
python 2026-MAI-Backend-I-Lyapin/lesson-05/smoke_test.py
```

Ожидаемый вывод: `OK`.

## Запуск проекта
SQLite (без Postgres):

```bash
$env:USE_SQLITE="1"
python 2026-MAI-Backend-I-Lyapin/project/manage.py migrate
python 2026-MAI-Backend-I-Lyapin/project/manage.py runserver 127.0.0.1:8001
```

Проверка:
- `http://127.0.0.1:8001/api/movies/`
- `http://127.0.0.1:8001/api/search/?q=silence`

## Пример POST-запроса (PowerShell)

```bash
$env:USE_SQLITE="1"
$body = '{ "title": "Test", "description": "Some silence here", "year": 2026 }'
Invoke-WebRequest -Method Post -Uri "http://127.0.0.1:8001/api/movies/create" -ContentType "application/json" -Body $body
```

