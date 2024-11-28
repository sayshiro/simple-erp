from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.metal import MetalType, MetalGost, MetalGrade, MetalProduct
from app.models.warehouse import Warehouse
from app.models.supplier import Supplier
from app import db
from flask_login import login_required
from app.forms.metal import MetalProductForm

bp = Blueprint('metal', __name__)

@bp.route('/metal')
@login_required
def index():
    """Показать список всех металлопрокатов"""
    products = MetalProduct.query.all()
    return render_template('metal/index.html', products=products)

@bp.route('/metal/add', methods=['GET', 'POST'])
@login_required
def add():
    """Добавить новый металлопрокат"""
    form = MetalProductForm()
    
    # Заполняем выпадающие списки данными
    form.type_id.choices = [(t.id, t.name) for t in MetalType.query.all()]
    form.gost_id.choices = [(g.id, g.number) for g in MetalGost.query.all()]
    form.grade_id.choices = [(g.id, g.name) for g in MetalGrade.query.all()]
    form.warehouse_id.choices = [(w.id, w.name) for w in Warehouse.query.all()]
    form.supplier_id.choices = [(s.id, s.name) for s in Supplier.query.all()]
    
    if form.validate_on_submit():
        try:
            product = MetalProduct(
                type_id=form.type_id.data,
                gost_id=form.gost_id.data,
                grade_id=form.grade_id.data,
                warehouse_id=form.warehouse_id.data,
                supplier_id=form.supplier_id.data,
                thickness=form.thickness.data,
                width=form.width.data,
                length=form.length.data,
                diameter=form.diameter.data,
                weight_per_unit=form.weight_per_unit.data,
                price_per_unit=form.price_per_unit.data,
                stock=form.stock.data
            )
            
            db.session.add(product)
            db.session.commit()
            flash('Металлопрокат успешно добавлен', 'success')
            return redirect(url_for('metal.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при добавлении металлопроката: {str(e)}', 'danger')
    
    return render_template('metal/add.html', form=form)

@bp.route('/metal/grades')
@login_required
def get_grades():
    """Получить список марок стали с их плотностями"""
    grades = MetalGrade.query.all()
    return jsonify({str(grade.id): grade.density for grade in grades})
