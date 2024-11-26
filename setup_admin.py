from app import create_app, db
from app.models import User
import sys

def create_admin_user():
    try:
        app = create_app()
        with app.app_context():
            # Проверяем, существует ли уже пользователь admin
            admin = User.query.filter_by(username='admin').first()
            if admin is None:
                # Создаем нового администратора
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin')
                db.session.add(admin)
                db.session.commit()
                print('Администратор успешно создан!')
                print('Логин: admin')
                print('Пароль: admin')
            else:
                print('Администратор уже существует')
    except Exception as e:
        print(f'Ошибка: {e}')
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    create_admin_user()
