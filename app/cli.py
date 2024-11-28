import click
from flask.cli import with_appcontext
from app import db
from app.models.initial_data import add_initial_data

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Инициализация базы данных."""
    db.create_all()
    click.echo('База данных создана.')
    
@click.command('add-test-data')
@with_appcontext
def add_test_data_command():
    """Добавление тестовых данных."""
    add_initial_data()
    click.echo('Тестовые данные добавлены.')
