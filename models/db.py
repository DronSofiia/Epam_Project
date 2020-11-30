from flask_sqlalchemy import SQLAlchemy

from service.app import app

DB_URI = 'postgresql+pg8000://sofii:sofii322@localhost:5432/corporation'


def get_db():
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    db = SQLAlchemy(app)
    db.engine.dialect.description_encoding = None
    return db
