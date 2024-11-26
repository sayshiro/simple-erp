from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired()])
    description = TextAreaField('Описание')
    price = DecimalField('Цена', validators=[DataRequired(), NumberRange(min=0)], places=2)
    stock = IntegerField('Количество на складе', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Сохранить')

class OrderItemForm(FlaskForm):
    product_id = SelectField('Товар', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Добавить в заказ')

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(p.id, f"{p.name} - {p.price}₽") 
                                 for p in Product.query.order_by(Product.name).all()]
