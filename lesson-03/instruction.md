# Lesson 03 — Django project + API stubs + nginx locations

## Что сделано
В репозитории уже есть Django-проект в папке `2026-MAI-Backend-I-Lyapin/project/` (тема: фильмы).
Для домашнего задания №3 добавлены заглушки API (через `JsonResponse`) и разведены URL под два location:
- `/web/` — простая HTML-страница (заглушка для web части)
- `/api/` — JSON API заглушки

Дополнительно: проект приведён к **чистому Django** (убрана зависимость от `djangorestframework`), чтобы он запускался после установки `requirements.txt` из корня репозитория.

## Реализованные URL
- `GET /web/` — HTML-страница со ссылками на API
- `GET /api/profile/` — заглушка профиля
- `GET /api/movies/` — заглушка “ленты” фильмов
- `GET /api/categories/<id>/` — заглушка страницы категории
- `POST /api/favorites/add/` — заглушка POST-метода (эхо принятого JSON)

Все методы ограничены декоратором `@require_http_methods`.

## Требования из задания (чеклист)
- [x] создать и запустить Django-проект
- [x] заглушки API через `JsonResponse` (profile, список сущностей, категория и т.д.)
- [x] разделить routes на два “location” будущего nginx: `/web/` и `/api/`
- [x] обрабатывать только нужные методы (GET/POST) через `@require_http_methods`

## Файлы
- `project/project/urls.py` — подключены `/web/` и `/api/`
- `project/project/views.py` — `main_view` (web)
- `project/movies/api_views.py` — заглушки API
- `project/movies/api_urls.py` — URL для API
- `lesson-03/nginx.conf` — пример конфига nginx с location `/web/` и `/api/`

## Как запустить (локально, без nginx)
### 1) Установить зависимости
Из корня репозитория:

```bash
pip install -r 2026-MAI-Backend-I-Lyapin/requirements.txt
```

### 2) Подготовить БД (SQLite для локального запуска)
Проект умеет запускаться на SQLite, чтобы не требовать Postgres для локальной проверки.

PowerShell:

```bash
$env:USE_SQLITE="1"
python 2026-MAI-Backend-I-Lyapin/project/manage.py migrate
```

### 3) Запустить Django
PowerShell:

```bash
$env:USE_SQLITE="1"
python 2026-MAI-Backend-I-Lyapin/project/manage.py runserver 127.0.0.1:8001
```

### 4) Открыть в браузере
- `http://127.0.0.1:8001/web/`
- `http://127.0.0.1:8001/api/profile/`

## Как подключить nginx
Используй `lesson-03/nginx.conf` как основу и направь `upstream` на адрес/порт Django (`127.0.0.1:8001` в примере).

## Быстрая проверка “что всё живо”
Из корня:

```bash
$env:USE_SQLITE="1"
python 2026-MAI-Backend-I-Lyapin/project/manage.py check
```

Ожидается: `System check identified no issues`.

## Частые проблемы
- `ModuleNotFoundError: django` → не установлен Django, поставь зависимости командой выше.
- Ошибка подключения к Postgres → для локального запуска включай `$env:USE_SQLITE="1"`.

