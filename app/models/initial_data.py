from app import db
from app.models.metal import MetalType, MetalGost, MetalGrade
from app.models.warehouse import Warehouse
from app.models.supplier import Supplier

def add_initial_data():
    # Добавляем типы металлопроката
    types = [
        MetalType(name='Лист'),
        MetalType(name='Труба круглая'),
        MetalType(name='Труба профильная'),
        MetalType(name='Уголок'),
        MetalType(name='Швеллер')
    ]
    
    # Добавляем ГОСТы
    gosts = [
        MetalGost(number='19903-2015', name='Прокат листовой горячекатаный'),
        MetalGost(number='10704-91', name='Трубы стальные электросварные прямошовные'),
        MetalGost(number='8639-82', name='Трубы стальные квадратные'),
        MetalGost(number='8509-93', name='Уголки стальные горячекатаные равнополочные'),
        MetalGost(number='8240-97', name='Швеллеры стальные горячекатаные')
    ]
    
    # Добавляем марки стали
    grades = [
        MetalGrade(name='Ст3', description='Углеродистая сталь обыкновенного качества'),
        MetalGrade(name='09Г2С', description='Низколегированная конструкционная сталь'),
        MetalGrade(name='20', description='Конструкционная углеродистая качественная сталь'),
        MetalGrade(name='45', description='Конструкционная углеродистая качественная сталь'),
        MetalGrade(name='40Х', description='Легированная конструкционная сталь')
    ]
    
    # Добавляем склады
    warehouses = [
        Warehouse(name='Основной склад', address='ул. Промышленная, 1'),
        Warehouse(name='Склад №2', address='ул. Заводская, 15')
    ]
    
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
    
    # Добавляем все в базу данных
    for items in [types, gosts, grades, warehouses, suppliers]:
        for item in items:
            db.session.add(item)
    
    try:
        db.session.commit()
        print("Начальные данные успешно добавлены")
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при добавлении данных: {str(e)}")
