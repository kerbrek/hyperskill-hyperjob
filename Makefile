.DEFAULT_GOAL := list

.PHONY: install
install:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

.PHONY: shell
shell:
	pipenv shell

.PHONY: check
check:
	pipenv run python manage.py check

.PHONY: check-deploy
check-deploy:
	pipenv run python manage.py check --deploy

.PHONY: run
run:
	pipenv run python manage.py runserver

.PHONY: makemigrations
makemigrations:
	pipenv run python manage.py makemigrations

.PHONY: migrate
migrate:
	pipenv run python manage.py migrate

.PHONY: createsuperuser
createsuperuser:
	pipenv run python manage.py createsuperuser

.PHONY: django-shell
django-shell:
	pipenv run python manage.py shell

.PHONY: requirements
requirements:
	pipenv lock -r > requirements.txt

.PHONY: up
up:
	docker-compose up --build

.PHONY: down
down:
	docker-compose down

.PHONY: up-dev
up-dev:
	docker-compose -f docker-compose.dev.yml up --build

.PHONY: down-dev
down-dev:
	docker-compose -f docker-compose.dev.yml down

.PHONY: up-debug
up-debug:
	docker-compose -f docker-compose.debug.yml up --build

.PHONY: down-debug
down-debug:
	docker-compose -f docker-compose.debug.yml down

# https://stackoverflow.com/a/26339924/6475258
.PHONY: list # Generate list of targets
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# https://stackoverflow.com/a/45843594/6475258
.PHONY: help # Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' $(lastword $(MAKEFILE_LIST)) | sed 's/\.PHONY: \(.*\) # \(.*\)/\1 - \2/'
