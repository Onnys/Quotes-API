import os
from sqlalchemy import Column, Integer, String, Text, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = os.environ['DATABASE_NAME']
database_path = os.environ['DATABASE_PATH']

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Authors(db.Model):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mail = Column(String, nullable=False)
    quotes = db.relationship('Quotes', backref='authors_quotes')

    def __init__(self, name, mail):
        self.name = name
        self.mail = mail

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'mail': self.mail
        }


class Quotes(db.Model):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    quote = Column(Text, nullable=False)
    author_id = Column(
        Integer, db.ForeignKey('authors.id'), nullable=False)

    def __init__(self, quote, author_id):
        self.quote = quote
        self.author_id = author_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'quote': self.quote,
            'author_id': self.author_id

        }
