#!/bin/sh

echo "Apply migrations..."
python manage.py migrate --noinput

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Create superuser automatically..."
python manage.py createsuperuser --noinput || true

echo "Starting server..."
gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
