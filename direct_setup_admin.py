from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User
import sys

try:
    print("Начинаем создание администратора...")
    
    # Создаем подключение к базе данных
    engine = create_engine('sqlite:///app.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("Подключение к базе данных установлено")

    # Проверяем существование админа
    admin = session.query(User).filter_by(username='admin').first()
    
    if admin is None:
        print("Создаем нового администратора...")
        # Создаем нового администратора
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin')
        session.add(admin)
        session.commit()
        print('Администратор успешно создан!')
        print('Логин: admin')
        print('Пароль: admin')
    else:
        print('Администратор уже существует')
    
    session.close()
    print("Сессия закрыта")
    sys.exit(0)
except Exception as e:
    print(f'Ошибка: {e}')
    sys.exit(1)
