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

makemigrations:
	pipenv run python manage.py makemigrations

migrate:
	pipenv run python manage.py migrate

createsuperuser:
	pipenv run python manage.py createsuperuser

django-shell:
	pipenv run python manage.py shell

.PHONY: install shell check check-deploy run makemigrations migrate createsuperuser django-shell
