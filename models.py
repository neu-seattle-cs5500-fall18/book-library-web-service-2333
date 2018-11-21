from flask_sqlalchemy import SQLAlchemy
import json
import datetime


def datetime_handler(x):
    if isinstance(x, datetime.date):
        return x.isoformat()
    raise TypeError("Unknown type")


db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_json(self):
        return json.dumps({'user_id': self.user_id, 'username': self.username})


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), unique=True, nullable=False)
    author = db.Column(db.String(100), unique=False, nullable=False)
    publish_date = db.Column(db.Date, unique=False, nullable=False)

    def __init__(self, name, author, publish_date):
        self.book_name = name
        self.author = author
        self.publish_date = publish_date

    def to_json(self):
        return json.dumps({'book_name': self.book_name, 'author': self.author,
                           'publish_date': self.publish_date}, default=datetime_handler)


class RentReturn(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(Book.book_id), unique=True, nullable=False)
    status = db.Column(db.Enum('RENT', 'RETURN'), unique=False, nullable=False)
    rent_date = db.Column(db.Date, unique=False, nullable=False)
    return_date = db.Column(db.Date, unique=False, nullable=True)

    def __init__(self, user_id, book_id, rent_date):
        self.user_id = user_id
        self.book_id = book_id
        self.status = 'RENT'
        self.rent_date = rent_date
        # self.return_date = None

    def to_json(self):
        return json.dumps({'user_id': self.user_id, 'book_id': self.book_id,
                           'status': self.status, 'rent_date': self.rent_date,
                           'return_date': self.return_date}, default=datetime_handler)
