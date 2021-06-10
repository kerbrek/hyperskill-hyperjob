install:
	env PIPENV_VENV_IN_PROJECT=1 pipenv install --dev

shell:
	pipenv shell

check:
	pipenv run python manage.py check

check-deploy:
	pipenv run python manage.py check --deploy

run:
	pipenv run python manage.py runserver

up:
	docker-compose up --build

down:
	docker-compose down

up-dev:
	docker-compose -f docker-compose.dev.yml up --build

down-dev:
	docker-compose -f docker-compose.dev.yml down

up-debug:
	docker-compose -f docker-compose.debug.yml up --build

down-debug:
	docker-compose -f docker-compose.debug.yml down

.PHONY: install shell check check-deploy run up down up-dev down-dev up-debug down-debug
