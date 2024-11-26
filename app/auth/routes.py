from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                current_app.logger.warning(f'Failed login attempt for non-existent user: {form.username.data}')
                flash('Пользователь с таким именем не найден', 'danger')
                return redirect(url_for('auth.login'))
            if not user.check_password(form.password.data):
                current_app.logger.warning(f'Failed login attempt for user: {user.username}')
                flash('Неверный пароль', 'danger')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            current_app.logger.info(f'Successful login for user: {user.username}')
            flash('Вы успешно вошли в систему', 'success')
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
    except Exception as e:
        current_app.logger.error(f'Error during login: {str(e)}', exc_info=True)
        flash('Произошла ошибка при входе в систему', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html', title='Вход', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)
