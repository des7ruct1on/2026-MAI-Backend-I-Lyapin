COMPOSE := docker compose -f lesson-06/docker-compose.yml

.PHONY: migrate build up down

migrate:
	$(COMPOSE) run --rm web python manage.py migrate

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down
