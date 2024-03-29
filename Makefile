.DEFAULT_GOAL := help

.PHONY: setup # Setup a working environment
setup:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
	pipenv run python manage.py migrate

.PHONY: shell # Spawn a shell within the virtual environment
shell:
	pipenv shell

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

## https://stackoverflow.com/a/45843594/6475258
.PHONY: help # Print list of targets with descriptions
help:
	@grep '^.PHONY: .* #' $(lastword $(MAKEFILE_LIST)) | sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' | expand -t20

## https://stackoverflow.com/a/26339924/6475258
# .PHONY: list # Print list of targets
# list:
# 	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
