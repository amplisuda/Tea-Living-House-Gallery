from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Image(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     vk_id = db.Column(db.String(50), unique=True, nullable=False)
#     title = db.Column(db.String(200), nullable=True)
#     url = db.Column(db.String(500), nullable=False)
#     category = db.Column(db.String(100), nullable=True)
#     upload_date = db.Column(db.DateTime, nullable=True)