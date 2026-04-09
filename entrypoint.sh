#!/bin/sh

echo "🚀 Running migrations..."
python manage.py migrate --noinput

echo "👤 Creating superuser (if not exists)..."
python create_superuser.py || true

echo "🌐 Starting Gunicorn..."
gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
