from flask import render_template
from app.main import bp
from app.models.metal import MetalProduct
from app.models.warehouse import Warehouse
from app.models.supplier import Supplier

@bp.route('/')
@bp.route('/index')
def index():
    """Главная страница"""
    stats = {
        'total_products': MetalProduct.query.count(),
        'total_orders': 0,  # Пока у нас нет модели заказов
        'total_suppliers': Supplier.query.count(),
        'total_categories': 0  # Пока у нас нет категорий
    }
    return render_template('index.html', title='Главная', stats=stats)
