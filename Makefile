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

.PHONY: install shell check check-deploy run
