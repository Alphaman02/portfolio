# Alpha Ndlangamandla - Portfolio (Django)

## Run it (Windows)
1. Unzip the project and open the folder that contains `manage.py` and `run.bat`.
2. Double-click `run.bat`. The first run takes a minute.
3. When asked, create your admin username and password.
4. Your site opens at http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/ (upload your photo and CV, edit project descriptions).

Next time just double-click `run.bat` again.

## Run it manually
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations portfolio
python manage.py migrate
python manage.py seed_portfolio
python manage.py createsuperuser
python manage.py runserver
```

## Before putting it online
Set `DEBUG = False`, a new `SECRET_KEY` and `ALLOWED_HOSTS` in `config/settings.py`, and run `python manage.py collectstatic`.

## Deploy on Render
See `DEPLOY.md` for the step-by-step guide.
