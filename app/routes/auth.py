from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login')
def login():
    return "Login page"  # Заглушка, так как у нас уже есть auth в другом месте
