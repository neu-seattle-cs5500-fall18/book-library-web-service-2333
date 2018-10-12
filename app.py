from flask import Flask, render_template, url_for, jsonify
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Book Store API',
    description='A simple Book Store API',
)

books = api.model('Book', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'book_name': fields.String(required=True, description='The task details')
})


class BookDAO(object):
    def __init__(self):
        self.counter = 0
        self.books = []

    def get(self, id):
        for book in self.books:
            if book['id'] == id:
                return book
        api.abort(404, "Book {} doesn't exist".format(id))

    def create(self, data):
        book = data
        book['id'] = self.counter = self.counter + 1
        self.books.append(book)
        return book

    def update(self, id, data):
        book = self.get(id)
        book.update(data)
        return book

    def delete(self, id):
        book = self.get(id)
        self.books.remove(book)


DAO = BookDAO()
DAO.create({'book_name': 'book1'})
DAO.create({'book_name': 'book2'})
DAO.create({'book_name': 'book3'})


@api.route('/books')
class BookStore(Resource):
    def get(self):
        return DAO.books

    def post(self):
        '''Create a new book'''
        return DAO.create({'book_name': 'new book'}), 201


@api.route('/book/<int:id>')
class Book(Resource):
    def get(self, id):
        return DAO.get(id)

    def delete(self, id):
        '''Delete a book given its identifier'''
        DAO.delete(id)
        return '', 204

    def put(self, id):
        '''Update a book given its identifier'''
        return DAO.update(id, api.payload)



if __name__ == '__main__':
    app.run(debug=True)
