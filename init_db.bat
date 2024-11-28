@echo off
set FLASK_APP=wsgi:app
flask init-db
flask add-test-data
pause
