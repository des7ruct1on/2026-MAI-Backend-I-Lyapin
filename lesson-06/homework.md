# Домашнее задание №6

## Установить docker и docker-compose (1 балл);
Например, как установить на [Ubuntu](https://docs.docker.com/engine/install/ubuntu/) или [MacOS](https://docs.docker.com/desktop/install/mac-install/).
## Создание Dockerfile для Django приложения (2 балла);
У нас уже есть приложение. Не забудем обновить requirements.txt с установленными питоновскими пакетами.
Нам нужно создать Dockerfile, который собрал бы образ нашего приложения. Важно помнить, что мы будем ходить в БД, как минимум.

## Создание docker-compose для проекта:
- nginx (2 балла),
- Django-приложение (2 балла)
- База данных (2 балла),
- Обязательно прописать depends\_on и healthcheck для каждого контейнера.

## Создание Makefile для проекта (1 балл);

Преподаватель должен иметь возможность, имея установленными только git,
docker и docker-compose склонировать проект, выполнить команды `make
migrate` и увидеть успешную миграцию.

curl -sS -G "http://127.0.0.1:8080/api/search/" --data-urlencode "q=lol"
curl -sS -X POST "http://127.0.0.1:8001/api/products/create/" -H "Content-Type: application/json" -d '{"title":"test111","description":"descr-test","price":111,"category_title":"test_cat"}'

docker compose -f lesson-06/docker-compose.yml down

docker compose -f lesson-06/docker-compose.yml up --build -d