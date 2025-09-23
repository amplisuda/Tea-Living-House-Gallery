from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Таблица для хранения сырых данных
class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    vk_id = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(2000), nullable=True)
    url = db.Column(db.String(1500), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    upload_date = db.Column(db.DateTime, nullable=True)


# Таблица для хранения категорий
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    parent = db.relationship('Category', remote_side=[id], backref='children')


# Таблица для хранения товаров
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(9999), nullable=False)
    price = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', backref='products')
    hash = db.Column(db.Text, unique=True)
    main_url = db.Column(db.Text, nullable=False)
    # hash = db.Column(db.Integer, db.ForeignKey('product_dict.hash'), nullable=True)
