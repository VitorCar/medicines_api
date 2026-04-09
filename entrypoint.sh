#!/bin/sh

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collect static..."
python manage.py collectstatic --noinput

echo "Checking superuser..."

python manage.py shell << END
from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.getenv("DJANGO_SUPERUSER_USERNAME")

if username and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=os.getenv("DJANGO_SUPERUSER_EMAIL"),
        password=os.getenv("DJANGO_SUPERUSER_PASSWORD")
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")
END

echo "Starting Gunicorn..."
gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
