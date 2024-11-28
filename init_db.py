from app import create_app, db
from app.models.initial_data import add_initial_data

app = create_app()

with app.app_context():
    # Создаем все таблицы
    db.create_all()
    print("База данных создана")
    
    # Добавляем тестовые данные
    add_initial_data()
    print("Тестовые данные добавлены")
