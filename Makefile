.DEFAULT_GOAL := help

.PHONY: install # Setup a virtual environment using Pipenv
install:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

.PHONY: shell # Spawn a shell within the virtual environment
shell:
	pipenv shell

.PHONY: test # Run tests
test:
	pipenv run pytest

.PHONY: lint # Run linter
lint:
	pipenv run pylint -d duplicate-code hyperjob/ resume/ vacancy/

.PHONY: check # Inspect Django project for common problems
check:
	pipenv run python manage.py check

.PHONY: run # Start a development Web server
run:
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

.PHONY: django-shell # Start the Python interactive interpreter
django-shell:
	pipenv run python manage.py shell

.PHONY: requirements # Generate requirements.txt file
requirements:
	pipenv lock -r > requirements.txt

# https://stackoverflow.com/a/26339924/6475258
.PHONY: list # Generate list of targets
list:
	@LC_ALL=C $(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# https://stackoverflow.com/a/45843594/6475258
.PHONY: help # Generate list of targets with descriptions
help:
	@grep '^.PHONY: .* #' $(lastword $(MAKEFILE_LIST)) | sed 's/\.PHONY: \(.*\) # \(.*\)/\1	\2/' | expand -t20
