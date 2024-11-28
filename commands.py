import click
from flask.cli import with_appcontext
from app import db
from app.models.metal import MetalType, MetalGost, MetalGrade
from app.models.warehouse import Warehouse
from app.models.supplier import Supplier
from app.models import User

@click.command('init-db')
@with_appcontext
def init_db():
    """Создать новые таблицы"""
    db.create_all()
    click.echo('База данных инициализирована.')

@click.command('add-test-data')
@with_appcontext
def add_test_data():
    """Добавить тестовые данные"""
    # Добавляем типы металлопроката
    types = [
        MetalType(name='Лист'),
        MetalType(name='Труба круглая'),
        MetalType(name='Труба профильная'),
        MetalType(name='Уголок'),
        MetalType(name='Швеллер')
    ]
    for t in types:
        db.session.add(t)
    db.session.commit()
    click.echo('Типы металлопроката добавлены.')

    # Добавляем ГОСТы
    gosts = [
        MetalGost(number='19903-2015', name='Прокат листовой горячекатаный'),
        MetalGost(number='10704-91', name='Трубы стальные электросварные прямошовные'),
        MetalGost(number='8639-82', name='Трубы стальные квадратные'),
        MetalGost(number='8509-93', name='Уголки стальные горячекатаные равнополочные'),
        MetalGost(number='8240-97', name='Швеллеры стальные горячекатаные')
    ]
    for g in gosts:
        db.session.add(g)
    db.session.commit()
    click.echo('ГОСТы добавлены.')

    # Добавляем марки стали
    grades = [
        MetalGrade(name='Ст3', description='Углеродистая сталь обыкновенного качества'),
        MetalGrade(name='09Г2С', description='Низколегированная конструкционная сталь'),
        MetalGrade(name='20', description='Конструкционная углеродистая качественная сталь'),
        MetalGrade(name='45', description='Конструкционная углеродистая качественная сталь'),
        MetalGrade(name='40Х', description='Легированная конструкционная сталь')
    ]
    for g in grades:
        db.session.add(g)
    db.session.commit()
    click.echo('Марки стали добавлены.')

    # Добавляем склады
    warehouses = [
        Warehouse(name='Основной склад', address='ул. Промышленная, 1'),
        Warehouse(name='Склад №2', address='ул. Заводская, 15')
    ]
    for w in warehouses:
        db.session.add(w)
    db.session.commit()
    click.echo('Склады добавлены.')

    # Добавляем поставщиков
    suppliers = [
        Supplier(
            name='МеталлТорг',
            contact_person='Иванов Иван',
            phone='+7 (999) 123-45-67',
            email='info@metaltorg.ru'
        ),
        Supplier(
            name='СтальПром',
            contact_person='Петров Петр',
            phone='+7 (999) 765-43-21',
            email='sales@stalprom.ru'
        )
    ]
    for s in suppliers:
        db.session.add(s)
    db.session.commit()
    click.echo('Поставщики добавлены.')

    # Добавляем тестового пользователя
    user = User(username='admin', email='admin@example.com', is_admin=True)
    user.set_password('admin')
    db.session.add(user)
    db.session.commit()
    click.echo('Тестовый пользователь добавлен (логин: admin, пароль: admin)')
