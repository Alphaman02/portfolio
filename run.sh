#!/usr/bin/env bash
# One-command setup and start for macOS/Linux.
set -e
cd "$(dirname "$0")"
[ -d venv ] || python3 -m venv venv
source venv/bin/activate
python -m pip install -q -r requirements.txt
python manage.py makemigrations portfolio
python manage.py migrate
python manage.py seed_portfolio
if [ ! -f .admin_created ]; then
  python manage.py createsuperuser && touch .admin_created
fi
python manage.py runserver
