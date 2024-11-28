from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class MetalProductForm(FlaskForm):
    type_id = SelectField('Тип металла', coerce=int, validators=[DataRequired()])
    gost_id = SelectField('ГОСТ', coerce=int, validators=[DataRequired()])
    grade_id = SelectField('Марка', coerce=int, validators=[DataRequired()])
    warehouse_id = SelectField('Склад', coerce=int, validators=[DataRequired()])
    supplier_id = SelectField('Поставщик', coerce=int, validators=[DataRequired()])
    
    thickness = FloatField('Толщина (мм)', validators=[Optional()])
    width = FloatField('Ширина (мм)', validators=[Optional()])
    length = FloatField('Длина (мм)', validators=[Optional()])
    diameter = FloatField('Диаметр (мм)', validators=[Optional()])
    
    weight_per_unit = FloatField('Вес единицы (кг)', validators=[Optional()])
    price_per_unit = FloatField('Цена за единицу', validators=[DataRequired()])
    stock = FloatField('Количество на складе', validators=[DataRequired()])
    
    submit = SubmitField('Сохранить')
