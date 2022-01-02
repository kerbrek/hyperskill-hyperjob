.DEFAULT_GOAL := help

SHELL := /usr/bin/env bash

project := hyperjob

.PHONY: setup # Setup a working environment
setup:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
	pipenv run python manage.py migrate

.PHONY: shell # Spawn a shell within the virtual environment
shell:
	env PIPENV_DOTENV_LOCATION=.env.example pipenv shell

.PHONY: test # Run tests
test:
	pipenv run pytest

.PHONY: coverage # Run tests with coverage report
coverage:
	pipenv run pytest --cov-report term-missing:skip-covered --cov=hyperjob --cov=resume --cov=vacancy

.PHONY: lint # Run linter
lint:
	pipenv run pylint -d duplicate-code hyperjob/ resume/ vacancy/

.PHONY: check # Inspect Django project for common problems
check:
	pipenv run python manage.py check

.PHONY: start # Start a development Web server
start:
	pipenv run python manage.py runserver

.PHONY: makemigrations # Generate Django migrations
makemigrations:
	pipenv run python manage.py makemigrations

.PHONY: migrate # Apply Django migrations
migrate:
	pipenv run python manage.py migrate

.PHONY: createsuperuser # Create Django superuser account
createsuperuser:
	pipenv run python manage.py createsuperuser

.PHONY: django-shell # Start Python interactive interpreter
django-shell:
	pipenv run python manage.py shell

.PHONY: requirements # Generate requirements.txt file
requirements:
	pipenv lock --requirements > requirements.txt

.PHONY: prepare-temp-containers
prepare-temp-containers:
	@echo Starting db container...
	@docker run -d --rm --name ${project}_temp_db --env-file ./.env.example -p 5432:5432 postgres:13-alpine

stop-prepared-temp-containers := echo; \
	echo Stopping db container...; \
	docker stop ${project}_temp_db

.PHONY: db # Start Postgres container
db: prepare-temp-containers
	@trap '${stop-prepared-temp-containers}' EXIT && \
		echo Press CTRL+C to stop && \
		sleep 1d

.PHONY: up # Start Compose services
up:
	docker-compose pull db nginx
	docker-compose build --pull
	docker-compose up

.PHONY: down # Stop Compose services
down:
	docker-compose down

.PHONY: up-dev # Start Compose services (development)
up-dev:
	docker-compose -f docker-compose.dev.yml pull db
	docker-compose -f docker-compose.dev.yml build --pull
	docker-compose -f docker-compose.dev.yml up

.PHONY: down-dev # Stop Compose services (development)
down-dev:
	docker-compose -f docker-compose.dev.yml down

.PHONY: up-debug # Start Compose services (debug)
up-debug:
	docker-compose -f docker-compose.debug.yml pull db
	docker-compose -f docker-compose.debug.yml build --pull
	docker-compose -f docker-compose.debug.yml up

.PHONY: down-debug # Stop Compose services (debug)
down-debug:
	docker-compose -f docker-compose.debug.yml down

.PHONY: help # Print list of targets with descriptions
help:
	@echo; \
		for mk in $(MAKEFILE_LIST); do \
			echo \# $$mk; \
			grep '^.PHONY: .* #' $$mk | sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' | expand -t20; \
			echo; \
		done
