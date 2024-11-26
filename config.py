import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    DEBUG = True
    TESTING = True  # Добавляем режим тестирования для более подробных сообщений об ошибках
    
    # SQLAlchemy config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Login config
    LOGIN_DISABLED = False
    
    # Logging config
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
