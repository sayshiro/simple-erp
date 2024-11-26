from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.models import User
from app.admin.forms import UserEditForm
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('У вас нет прав для доступа к этой странице.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def index():
    return render_template('admin/index.html', title='Админ панель')

@bp.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    query = User.query
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            (User.username.ilike(search)) |
            (User.email.ilike(search))
        )
    
    users = query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('admin/users.html', title='Управление пользователями', 
                         users=users, search=search)

@bp.route('/user/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserEditForm(original_username=user.username, original_email=user.email)
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.is_admin.data = user.is_admin
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('Пользователь успешно обновлен.', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/edit_user.html', title='Редактирование пользователя', 
                         form=form, user=user)

@bp.route('/user/<int:id>/toggle_admin')
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('Вы не можете изменить свои собственные права администратора.', 'error')
    else:
        user.is_admin = not user.is_admin
        db.session.commit()
        flash(f'Права администратора для пользователя {user.username} {"предоставлены" if user.is_admin else "отозваны"}.', 'success')
    return redirect(url_for('admin.users'))

@bp.route('/user/<int:id>/delete')
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash('Вы не можете удалить свой собственный аккаунт.', 'error')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(f'Пользователь {user.username} удален.', 'success')
    return redirect(url_for('admin.users'))
