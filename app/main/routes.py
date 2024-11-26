from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.forms import ProductForm, OrderItemForm, SupplierForm, CategoryForm, WarehouseForm, InventoryMovementForm
from app.models import Product, Order, OrderItem, Supplier, ProductCategory, Warehouse, InventoryMovement

@bp.route('/')
@bp.route('/index')
def index():
    stats = {
        'total_products': Product.query.count(),
        'total_orders': Order.query.count(),
        'total_suppliers': Supplier.query.count(),
        'total_categories': ProductCategory.query.count()
    }
    
    # Получаем последние заказы
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Получаем товары с низким запасом
    low_stock_products = Product.query.filter(Product.stock <= Product.minimum_stock).limit(5).all()
    
    return render_template('index.html', 
                         title='Главная',
                         stats=stats,
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products)

@bp.route('/products')
@login_required
def products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.name).paginate(
        page=page, per_page=10, error_out=False)
    return render_template('main/products.html', title='Товары', products=products)

@bp.route('/product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('У вас нет прав для добавления товаров')
        return redirect(url_for('main.products'))
    
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data
        )
        db.session.add(product)
        db.session.commit()
        flash('Товар успешно добавлен')
        return redirect(url_for('main.products'))
    return render_template('main/product_form.html', title='Добавить товар', form=form)

@bp.route('/product/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if not current_user.is_admin:
        flash('У вас нет прав для редактирования товаров')
        return redirect(url_for('main.products'))
    
    product = Product.query.get_or_404(id)
    form = ProductForm()
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.stock = form.stock.data
        db.session.commit()
        flash('Товар успешно обновлен')
        return redirect(url_for('main.products'))
    elif request.method == 'GET':
        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.stock.data = product.stock
    return render_template('main/product_form.html', title='Редактировать товар', form=form)

@bp.route('/product/<int:id>/delete')
@login_required
def delete_product(id):
    if not current_user.is_admin:
        flash('У вас нет прав для удаления товаров')
        return redirect(url_for('main.products'))
    
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Товар успешно удален')
    return redirect(url_for('main.products'))

@bp.route('/orders')
@login_required
def orders():
    page = request.args.get('page', 1, type=int)
    if current_user.is_admin:
        orders = Order.query.order_by(Order.created_at.desc()).paginate(
            page=page, per_page=10, error_out=False)
    else:
        orders = Order.query.filter_by(user_id=current_user.id).order_by(
            Order.created_at.desc()).paginate(page=page, per_page=10, error_out=False)
    return render_template('main/orders.html', title='Заказы', orders=orders)

@bp.route('/order/new', methods=['GET', 'POST'])
@login_required
def new_order():
    # Создаем новый заказ
    order = Order(user_id=current_user.id, status='pending', total_amount=0)
    db.session.add(order)
    db.session.commit()
    flash('Заказ создан. Теперь добавьте товары.')
    return redirect(url_for('main.edit_order', id=order.id))

@bp.route('/order/<int:id>')
@login_required
def view_order(id):
    order = Order.query.get_or_404(id)
    if not current_user.is_admin and order.user_id != current_user.id:
        flash('У вас нет доступа к этому заказу')
        return redirect(url_for('main.orders'))
    return render_template('main/order_detail.html', title='Просмотр заказа', order=order)

@bp.route('/order/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    if not current_user.is_admin and order.user_id != current_user.id:
        flash('У вас нет доступа к этому заказу')
        return redirect(url_for('main.orders'))
    
    if order.status != 'pending':
        flash('Нельзя редактировать подтвержденный заказ')
        return redirect(url_for('main.view_order', id=id))

    form = OrderItemForm()
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        if product.stock < form.quantity.data:
            flash(f'Недостаточно товара на складе. Доступно: {product.stock}')
            return redirect(url_for('main.edit_order', id=id))
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=form.quantity.data,
            price=product.price
        )
        # Обновляем количество на складе
        product.stock -= form.quantity.data
        # Обновляем общую сумму заказа
        order.total_amount += product.price * form.quantity.data
        
        db.session.add(order_item)
        db.session.commit()
        flash('Товар добавлен в заказ')
        return redirect(url_for('main.edit_order', id=id))
    
    return render_template('main/order_edit.html', title='Редактирование заказа', 
                         order=order, form=form)

@bp.route('/order/<int:id>/remove_item/<int:item_id>')
@login_required
def remove_order_item(id, item_id):
    order = Order.query.get_or_404(id)
    if not current_user.is_admin and order.user_id != current_user.id:
        flash('У вас нет доступа к этому заказу')
        return redirect(url_for('main.orders'))
    
    if order.status != 'pending':
        flash('Нельзя редактировать подтвержденный заказ')
        return redirect(url_for('main.view_order', id=id))

    item = OrderItem.query.get_or_404(item_id)
    if item.order_id != order.id:
        flash('Товар не принадлежит этому заказу')
        return redirect(url_for('main.edit_order', id=id))
    
    # Возвращаем товар на склад
    product = Product.query.get(item.product_id)
    product.stock += item.quantity
    # Обновляем общую сумму заказа
    order.total_amount -= item.price * item.quantity
    
    db.session.delete(item)
    db.session.commit()
    flash('Товар удален из заказа')
    return redirect(url_for('main.edit_order', id=id))

@bp.route('/order/<int:id>/confirm')
@login_required
def confirm_order(id):
    order = Order.query.get_or_404(id)
    if not current_user.is_admin and order.user_id != current_user.id:
        flash('У вас нет доступа к этому заказу')
        return redirect(url_for('main.orders'))
    
    if not order.items:
        flash('Нельзя подтвердить пустой заказ')
        return redirect(url_for('main.edit_order', id=id))
    
    order.status = 'confirmed'
    db.session.commit()
    flash('Заказ подтвержден')
    return redirect(url_for('main.view_order', id=id))

@bp.route('/order/<int:id>/cancel')
@login_required
def cancel_order(id):
    order = Order.query.get_or_404(id)
    if not current_user.is_admin and order.user_id != current_user.id:
        flash('У вас нет доступа к этому заказу')
        return redirect(url_for('main.orders'))
    
    if order.status != 'pending':
        flash('Нельзя отменить подтвержденный заказ')
        return redirect(url_for('main.view_order', id=id))
    
    # Возвращаем все товары на склад
    for item in order.items:
        product = Product.query.get(item.product_id)
        product.stock += item.quantity
    
    db.session.delete(order)
    db.session.commit()
    flash('Заказ отменен')
    return redirect(url_for('main.orders'))

# Маршруты для работы с поставщиками
@bp.route('/suppliers')
@login_required
def suppliers():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template('main/suppliers.html', title='Поставщики', suppliers=suppliers)

@bp.route('/supplier/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not current_user.is_admin:
        flash('У вас нет прав для добавления поставщиков')
        return redirect(url_for('main.suppliers'))
    
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            contact_person=form.contact_person.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Поставщик успешно добавлен')
        return redirect(url_for('main.suppliers'))
    return render_template('main/supplier_form.html', title='Добавить поставщика', form=form)

@bp.route('/supplier/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_supplier(id):
    if not current_user.is_admin:
        flash('У вас нет прав для редактирования поставщиков')
        return redirect(url_for('main.suppliers'))
    
    supplier = Supplier.query.get_or_404(id)
    form = SupplierForm()
    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.contact_person = form.contact_person.data
        supplier.email = form.email.data
        supplier.phone = form.phone.data
        supplier.address = form.address.data
        db.session.commit()
        flash('Поставщик успешно обновлен')
        return redirect(url_for('main.suppliers'))
    elif request.method == 'GET':
        form.name.data = supplier.name
        form.contact_person.data = supplier.contact_person
        form.email.data = supplier.email
        form.phone.data = supplier.phone
        form.address.data = supplier.address
    return render_template('main/supplier_form.html', title='Редактировать поставщика', form=form)

# Маршруты для работы с категориями
@bp.route('/categories')
@login_required
def categories():
    categories = ProductCategory.query.filter_by(parent_id=None).all()
    return render_template('main/categories.html', title='Категории', categories=categories)

@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if not current_user.is_admin:
        flash('У вас нет прав для добавления категорий')
        return redirect(url_for('main.categories'))
    
    form = CategoryForm()
    form.parent_id.choices = [(0, '-- Нет --')] + [(c.id, c.name) for c in ProductCategory.query.all()]
    
    if form.validate_on_submit():
        category = ProductCategory(
            name=form.name.data,
            description=form.description.data,
            parent_id=form.parent_id.data if form.parent_id.data != 0 else None
        )
        db.session.add(category)
        db.session.commit()
        flash('Категория успешно добавлена')
        return redirect(url_for('main.categories'))
    return render_template('main/category_form.html', title='Добавить категорию', form=form)

# Маршруты для работы со складами
@bp.route('/warehouses')
@login_required
def warehouses():
    warehouses = Warehouse.query.order_by(Warehouse.name).all()
    return render_template('main/warehouses.html', title='Склады', warehouses=warehouses)

@bp.route('/warehouse/add', methods=['GET', 'POST'])
@login_required
def add_warehouse():
    if not current_user.is_admin:
        flash('У вас нет прав для добавления складов')
        return redirect(url_for('main.warehouses'))
    
    form = WarehouseForm()
    if form.validate_on_submit():
        warehouse = Warehouse(
            name=form.name.data,
            address=form.address.data,
            capacity=form.capacity.data
        )
        db.session.add(warehouse)
        db.session.commit()
        flash('Склад успешно добавлен')
        return redirect(url_for('main.warehouses'))
    return render_template('main/warehouse_form.html', title='Добавить склад', form=form)

# Маршруты для работы с движением товаров
@bp.route('/inventory')
@login_required
def inventory():
    movements = InventoryMovement.query.order_by(InventoryMovement.created_at.desc()).all()
    return render_template('main/inventory.html', title='Движение товаров', movements=movements)

@bp.route('/inventory/add', methods=['GET', 'POST'])
@login_required
def add_movement():
    if not current_user.is_admin:
        flash('У вас нет прав для добавления движения товаров')
        return redirect(url_for('main.inventory'))
    
    form = InventoryMovementForm()
    form.product_id.choices = [(p.id, p.name) for p in Product.query.order_by(Product.name).all()]
    form.warehouse_id.choices = [(w.id, w.name) for w in Warehouse.query.order_by(Warehouse.name).all()]
    
    if form.validate_on_submit():
        movement = InventoryMovement(
            product_id=form.product_id.data,
            warehouse_id=form.warehouse_id.data,
            quantity=form.quantity.data,
            movement_type=form.movement_type.data,
            reference=form.reference.data,
            created_by=current_user.id
        )
        
        # Обновляем остаток товара
        product = Product.query.get(form.product_id.data)
        if form.movement_type.data == 'in':
            product.stock += form.quantity.data
        elif form.movement_type.data == 'out':
            if product.stock < form.quantity.data:
                flash('Недостаточно товара на складе')
                return render_template('main/movement_form.html', title='Добавить движение', form=form)
            product.stock -= form.quantity.data
        
        db.session.add(movement)
        db.session.commit()
        flash('Движение товара успешно добавлено')
        return redirect(url_for('main.inventory'))
    return render_template('main/movement_form.html', title='Добавить движение', form=form)
