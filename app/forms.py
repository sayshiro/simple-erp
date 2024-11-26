from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class SupplierForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    contact_person = StringField('Контактное лицо')
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Телефон')
    address = TextAreaField('Адрес')
    submit = SubmitField('Сохранить')

class ProductForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    price = FloatField('Цена', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    minimum_stock = IntegerField('Минимальный запас', default=0)
    category_id = SelectField('Категория', coerce=int)
    supplier_id = SelectField('Поставщик', coerce=int)
    submit = SubmitField('Сохранить')

class CategoryForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    parent_id = SelectField('Родительская категория', coerce=int, validators=[Optional()])
    submit = SubmitField('Сохранить')

class WarehouseForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    address = TextAreaField('Адрес')
    capacity = FloatField('Вместимость (м²)')
    submit = SubmitField('Сохранить')

class InventoryMovementForm(FlaskForm):
    product_id = SelectField('Продукт', coerce=int, validators=[DataRequired()])
    warehouse_id = SelectField('Склад', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    movement_type = SelectField('Тип движения', 
                              choices=[('in', 'Приход'), 
                                     ('out', 'Расход'), 
                                     ('transfer', 'Перемещение')])
    reference = StringField('Номер документа')
    submit = SubmitField('Сохранить')

class OrderItemForm(FlaskForm):
    product_id = SelectField('Товар', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    submit = SubmitField('Добавить')
