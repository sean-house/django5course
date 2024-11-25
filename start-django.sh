#!/bin/bash
poetry run python manage.py collectstatic --no-input
poetry run python manage.py migrate

if [[ "$ENV_STATE" == "production" ]]; then
    echo "Running in production mode"
    poetry run gunicorn django5course.wsgi --workers $GUNICORN_WORKERS --forwarded-allow-ips "*" --log-level "debug"
else
    echo "Running in development mode"
    poetry run python manage.py runserver 0.0.0.0:8000
fi
