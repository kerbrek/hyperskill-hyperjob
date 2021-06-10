#!/bin/bash

python manage.py collectstatic --noinput
./wait-for-it.sh "${POSTGRES_HOST}:${POSTGRES_PORT}"
python manage.py migrate --noinput

exec "$@"
