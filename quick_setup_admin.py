import sqlite3
import sys
from werkzeug.security import generate_password_hash

def create_admin():
    try:
        # Подключаемся к базе данных напрямую через sqlite3
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        # Проверяем существование админа
        cursor.execute("SELECT id FROM user WHERE username = ?", ('admin',))
        admin = cursor.fetchone()
        
        if admin is None:
            # Создаем хеш пароля
            password_hash = generate_password_hash('admin')
            
            # Добавляем администратора
            cursor.execute("""
                INSERT INTO user (username, email, password_hash, is_admin)
                VALUES (?, ?, ?, ?)
            """, ('admin', 'admin@example.com', password_hash, True))
            
            conn.commit()
            print('Администратор успешно создан!')
            print('Логин: admin')
            print('Пароль: admin')
        else:
            print('Администратор уже существует')
        
        conn.close()
        return True
        
    except Exception as e:
        print(f'Ошибка: {e}')
        return False

if __name__ == '__main__':
    success = create_admin()
    sys.exit(0 if success else 1)
