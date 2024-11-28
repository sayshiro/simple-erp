from app import db
from datetime import datetime

class MetalType(db.Model):
    """Тип металлопроката (профиль)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Например: Лист, Труба круглая, Уголок
    description = db.Column(db.Text)
    measurement_unit = db.Column(db.String(20))  # Единица измерения: метры, штуки, кг
    
    products = db.relationship('MetalProduct', backref='type')

class MetalGost(db.Model):
    """ГОСТ для металлопроката"""
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50), nullable=False, unique=True)  # Номер ГОСТа
    name = db.Column(db.String(200), nullable=False)  # Название ГОСТа
    description = db.Column(db.Text)
    metal_type_id = db.Column(db.Integer, db.ForeignKey('metal_type.id'))  # Связь с типом металлопроката
    
    metal_type = db.relationship('MetalType', backref='gosts')
    products = db.relationship('MetalProduct', backref='gost')

class MetalGrade(db.Model):
    """Марка металла"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Например: Ст3, 09Г2С
    density = db.Column(db.Float, nullable=False, default=7.85)  # плотность в г/см³, сталь по умолчанию
    description = db.Column(db.Text)
    properties = db.Column(db.JSON)  # Характеристики в формате JSON
    usage = db.Column(db.Text)  # Применение
    
    products = db.relationship('MetalProduct', backref='grade')

class MetalProduct(db.Model):
    """Конкретный металлопрокат"""
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('metal_type.id'), nullable=False)
    gost_id = db.Column(db.Integer, db.ForeignKey('metal_gost.id'), nullable=False)
    grade_id = db.Column(db.Integer, db.ForeignKey('metal_grade.id'), nullable=False)
    
    # Размеры
    thickness = db.Column(db.Float)  # Толщина (мм)
    width = db.Column(db.Float)      # Ширина (мм)
    length = db.Column(db.Float)     # Длина (мм)
    diameter = db.Column(db.Float)   # Диаметр (мм)
    
    weight_per_unit = db.Column(db.Float)  # Вес единицы (кг)
    price_per_unit = db.Column(db.Float)  # Цена за единицу (руб)
    stock = db.Column(db.Float, default=0)  # Количество на складе
    minimum_stock = db.Column(db.Float, default=0)  # Минимальный запас
    
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    warehouse = db.relationship('Warehouse', backref='metal_products')
    supplier = db.relationship('Supplier', backref='metal_products')

    def __repr__(self):
        return f'<MetalProduct {self.type.name} ГОСТ {self.gost.number} {self.grade.name}>'

    @property
    def full_name(self):
        """Полное наименование продукта"""
        dims = []
        if self.thickness is not None and self.thickness > 0:
            dims.append(f"т.{self.thickness}")
        if self.width is not None and self.width > 0:
            dims.append(f"ш.{self.width}")
        if self.length is not None and self.length > 0:
            dims.append(f"д.{self.length}")
        if self.diameter is not None and self.diameter > 0:
            dims.append(f"∅{self.diameter}")
        
        dimensions_str = "x".join(str(d) for d in dims) if dims else "-"
        return f"{self.type.name} {dimensions_str} {self.grade.name} ГОСТ {self.gost.number}"
