@echo off
REM One-click setup and start for Windows. Double-click this file.
cd /d "%~dp0"

set PY=python
where python >nul 2>nul || set PY=py

if not exist venv (
  echo Creating virtual environment...
  %PY% -m venv venv || goto :fail
)
call venv\Scripts\activate || goto :fail

echo Installing requirements...
python -m pip install -q -r requirements.txt || goto :fail

echo Setting up database...
python manage.py makemigrations portfolio || goto :fail
python manage.py migrate || goto :fail
python manage.py seed_portfolio || goto :fail

if not exist .admin_created (
  echo.
  echo Create your admin login. The password stays hidden while you type.
  python manage.py createsuperuser || goto :fail
  echo done> .admin_created
)

echo.
echo Starting site at http://127.0.0.1:8000/  (press Ctrl+C to stop)
start "" http://127.0.0.1:8000/
python manage.py runserver
goto :eof

:fail
echo.
echo Something went wrong. Scroll up, read the last error, and send it to Claude.
pause
