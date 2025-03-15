from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.String(50))
    price = db.Column(db.Float)
    appropriate_age = db.Column(db.String(50))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    image_url = db.Column(db.String(200))