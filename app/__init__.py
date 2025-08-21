from flask import Flask
from app.config import Config
from app.models import db
from app.blueprints.main.routes import main_bp
from app.blueprints.products.routes import products_bp
from app.blueprints.categories.routes import categories_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(products_bp, url_prefix='/product')
    app.register_blueprint(categories_bp, url_prefix='/categories')

    with app.app_context():
        db.create_all()

    return app