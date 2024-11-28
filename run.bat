@echo off
set FLASK_APP=wsgi:app
set FLASK_ENV=development
flask run --port=8080
pause
