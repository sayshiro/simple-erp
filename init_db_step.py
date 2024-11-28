from app import create_app, db
from app.models.metal import MetalType, MetalGost, MetalGrade
from app.models.warehouse import Warehouse
from app.models.supplier import Supplier

app = create_app()

with app.app_context():
    # Шаг 1: Создаем таблицы
    print("Создаем таблицы...")
    db.create_all()
    print("Таблицы созданы")

    # Шаг 2: Добавляем типы металлопроката
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
    print("Типы металлопроката добавлены")

    # Шаг 3: Добавляем ГОСТы
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
    print("ГОСТы добавлены")

    # Шаг 4: Добавляем марки стали
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
    print("Марки стали добавлены")

    # Шаг 5: Добавляем склады
    warehouses = [
        Warehouse(name='Основной склад', address='ул. Промышленная, 1'),
        Warehouse(name='Склад №2', address='ул. Заводская, 15')
    ]
    for w in warehouses:
        db.session.add(w)
    db.session.commit()
    print("Склады добавлены")

    # Шаг 6: Добавляем поставщиков
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
    print("Поставщики добавлены")

print("Все данные успешно добавлены!")
