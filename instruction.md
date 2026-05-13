# Домашние задания №5 и №6 (на базе `lesson-03/uniapp/`)

## ДЗ №5 — что требовалось

- Реализовать вьюхи вместо заглушек: работа с сущностями из БД.
- `GET /api/search/?q=...` — поиск по **минимум двум полям** (у нас: `title` и `description`), ответ `JsonResponse`.
- `GET /api/products/` — все объекты из БД, **только GET**, `JsonResponse`.
- `POST /api/products/create/` — создание объекта, **только POST**, `JsonResponse`.

Тематика проекта — каталог **продуктов** (`Product`), множественное число в URL: `products`.

## ДЗ №5 — что сделано

- В модель `Product` добавлено поле `description` (миграция `main/migrations/0003_product_description.py`).
- Реализованы вьюхи в `lesson-03/uniapp/main/views.py`:
  - `api_search` — фильтр `Q(title__icontains=q) | Q(description__icontains=q)`.
  - `api_products` — выборка всех продуктов с сериализацией в JSON.
  - `api_products_create` — разбор JSON из тела запроса, валидация, `201` при успехе.
- Роуты в `lesson-03/uniapp/main/api_urls.py` (важен порядок: `products/create/` раньше `products/`).
- Дополнительно: `api_category` переведён на данные из БД (не требование ДЗ‑5, но согласовано с моделями).
- В шаблоне `main/templates/main/index.html` добавлена ссылка на поиск.

### Формат `POST /api/products/create/`

Тело — JSON, поля:

- `title` (обязательно, строка)
- `category_id` (число, существующая категория) **или**
- `category_title` (строка): категория с таким названием будет **создана при отсутствии** (`get_or_create`) — можно не знать `id`
- `price` (целое, по умолчанию 0)
- `description` (строка, по умолчанию `""`)

Нужно передать **хотя бы одно** из полей `category_id` / `category_title`.

Если указан несуществующий `category_id` — ответ **`404`** с JSON `{"error":"category not found","category_id":...}`.

Если в `curl` подставляешь `category_id` из вывода `manage.py shell`, в тело запроса может попасть лишний текст (`objects imported` и т.п.) — получится **`{"error":"invalid json"}`**. Надёжнее: **`category_title`** или id из «чистого» вывода (пример с `python -c` ниже).

---

## Примеры `curl`: поиск и создание

Базовый URL:

- локально без Docker: `http://127.0.0.1:8001` (нужен запущенный `runserver`)
- Docker Compose: `http://127.0.0.1:8080` (через nginx) или **напрямую Gunicorn** `http://127.0.0.1:8001` (порт проброшен в `lesson-06/docker-compose.yml` как `8001:8001`)

Ниже в примерах используется **`BASE=http://127.0.0.1:8080`** для стека из `lesson-06`. Для прямого доступа к контейнеру `web` замени на `http://127.0.0.1:8001` (после `docker compose up` с актуальным compose).

### Поиск (`GET /api/search/?q=...`)

Латиница (параметр в кавычках, чтобы shell не съел `?`):

```bash
BASE=http://127.0.0.1:8080
curl -sS "${BASE}/api/search/?q=silence"
```

Кириллица и пробелы — через `--data-urlencode`, чтобы кодировка была корректной:

```bash
BASE=http://127.0.0.1:8080
curl -sS -G "${BASE}/api/search/" --data-urlencode "q=молчание"
```

Без параметра `q` ответ будет **`400`** с JSON `{"error":"missing q"}`.

### Список продуктов (`GET /api/products/`)

```bash
BASE=http://127.0.0.1:8080
curl -sS "${BASE}/api/products/"
```

### Создание продукта (`POST /api/products/create/`)

**Проще всего** — передать **`category_title`**: категория создастся сама, если её ещё не было (`get_or_create` по полю `title`, оно уникально в модели).

```bash
BASE=http://127.0.0.1:8080
curl -sS -X POST "${BASE}/api/products/create/" \
  -H "Content-Type: application/json" \
  -d '{"title":"X","description":"Y","price":10,"category_title":"Demo"}'
```

Тот же запрос на хосте **8001** (Gunicorn в Docker или локальный `runserver`):

```bash
curl -sS -X POST "http://127.0.0.1:8001/api/products/create/" \
  -H "Content-Type: application/json" \
  -d '{"title":"X","description":"Y","price":10,"category_title":"Demo"}'
```

**Вариант с `category_id`** — если id уже известен (например из админки). Узнать или создать категорию в контейнере и вывести только число `id` (из корня репозитория):

```bash
CID=$(docker compose -f lesson-06/docker-compose.yml exec -T web python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniapp.settings')
django.setup()
from main.models import Category
c, _ = Category.objects.get_or_create(title='Demo')
print(c.id)
")
echo "category_id=$CID"
curl -sS -X POST "http://127.0.0.1:8080/api/products/create/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"New item\",\"description\":\"Short text\",\"price\":99,\"category_id\":${CID}}"
```

Произвольный **`category_id` без строки в таблице `Category` задать нельзя**: это внешний ключ в реляционной БД — иначе база потеряла бы смысл ссылок.

После изменения compose перезапуск: `docker compose -f lesson-06/docker-compose.yml up -d`.

---

## ДЗ №6 — что требовалось

- Установить Docker и Docker Compose (у преподавателя/студента локально).
- `Dockerfile` для Django-приложения (учёт подключения к БД).
- `docker-compose`: **nginx**, **Django**, **БД**; у каждого сервиса — `depends_on` и `healthcheck`.
- `Makefile`: после клонирования репозитория команда `make migrate` должна успешно выполнить миграции.

## ДЗ №6 — что сделано

| Файл | Назначение |
|------|------------|
| `lesson-03/uniapp/Dockerfile` | Сборка образа web: Python 3.12, зависимости из корневого `requirements.txt`, копирование `lesson-03/uniapp` в `/app`, `gunicorn` на `8001`. |
| `lesson-06/docker-compose.yml` | Сервисы `db` (Postgres 16), `web` (build), `nginx` (прокси на `web:8001`); у всех трёх — `healthcheck`; цепочка `depends_on` с `condition: service_healthy`. |
| `lesson-06/nginx-docker.conf` | Конфиг nginx: upstream `web:8001`, `location /web/` и `/api/`. |
| `Makefile` (корень репозитория) | Цель `migrate`: `docker compose -f lesson-06/docker-compose.yml run --rm web python manage.py migrate`. |

Контейнер `web` при полном `docker compose up` запускает `migrate` и затем `gunicorn` (см. `command` в compose). Цель `make migrate` делает отдельный одноразовый прогон миграций (поднимает зависимости, в т.ч. здоровую БД).

---

## Структура (кратко): что вручную / что генерируется

- Писалось вручную: `main/views.py`, `main/api_urls.py`, `main/tests.py`, шаблоны, `Dockerfile`, `docker-compose.yml`, `nginx-docker.conf`, `Makefile`, этот `instruction.md`.
- Генерируется Django: `main/migrations/0003_product_description.py` (через `makemigrations`; файл в репозитории уже добавлен).

---

## Локальный запуск без Docker (проверка ДЗ‑5)

Из корня репозитория:

```bash
./venv/bin/python -m pip install -r requirements.txt
./venv/bin/python lesson-03/uniapp/manage.py migrate
./venv/bin/python lesson-03/uniapp/manage.py runserver 127.0.0.1:8001
```

Проверки в браузере:

- `http://127.0.0.1:8001/api/search/?q=silence`
- `http://127.0.0.1:8001/api/products/`

Примеры `curl` для поиска и создания — в разделе **«Примеры curl: поиск и создание»** выше.

## Тесты (выполнялись)

```bash
./venv/bin/python lesson-03/uniapp/manage.py test main
```

Результат: **5 тестов, OK** (поиск, список, запрет POST на список, create POST, запрет GET на create).

Проверка синтаксиса compose:

```bash
docker compose -f lesson-06/docker-compose.yml config
```

Результат: конфиг валиден.

Если `docker compose pull` / `up --build` падает с **TLS timeout** или **EOF** при обращении к `registry-1.docker.io`, это сетевая проблема до Docker Hub: повторить позже, сменить сеть/VPN/DNS, перезапустить Docker Desktop.

## Запуск стека Docker (ДЗ‑6)

Требования: установлены Docker и Docker Compose v2.

Из корня репозитория:

```bash
make migrate
```

или поднять всё и открыть сайт через nginx:

```bash
docker compose -f lesson-06/docker-compose.yml up --build -d
```

Nginx слушает **порт 8080** на хосте:

- `http://127.0.0.1:8080/web/`
- `http://127.0.0.1:8080/api/products/`
- `http://127.0.0.1:8080/api/search/?q=silence`
- напрямую к приложению в контейнере: `http://127.0.0.1:8001/api/products/` (проброс порта `web`)

Остановка:

```bash
make down
```

или

```bash
docker compose -f lesson-06/docker-compose.yml down
```
