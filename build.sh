#!/usr/bin/env bash
# Render build command:  bash build.sh
set -o errexit

pip install -r requirements-prod.txt
python manage.py collectstatic --no-input
python manage.py makemigrations portfolio --no-input
python manage.py migrate --no-input
python manage.py seed_portfolio --if-empty

# Create the admin login from environment variables (skipped if it already exists)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput --email "${DJANGO_SUPERUSER_EMAIL:-admin@example.com}" || true
fi
