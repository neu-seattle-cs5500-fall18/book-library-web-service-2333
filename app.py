from flask import Flask, render_template, url_for, jsonify
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Book Store API',
          description='A simple Book Store API')
ns_book = api.namespace('books', description='BOOK operations')
ns_user = api.namespace('users', description='USER operations')
ns_borrow = api.namespace('borrows', description='BORROW operations')

books = api.model('Book', {
    'id': fields.Integer(readOnly=True, description='The book unique identifier'),
    'book_name': fields.String(required=True, description='The book name')
})

users = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'username': fields.String(required=True, description='The username')
})

borrows = api.model('Borrow', {
    'id': fields.Integer(readOnly=True, description='The borrow unique identifier'),
    'book_id': fields.Integer(required=True, description='The book id'),
    'user_id': fields.Integer(required=True, description='The user id')
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


class UserDAO(object):
    def __init__(self):
        self.counter = 0
        self.users = []

    def get(self, id):
        for user in self.users:
            if user['id'] == id:
                return user
        api.abort(404, "Book {} doesn't exist".format(id))

    def create(self, data):
        user = data
        user['id'] = self.counter = self.counter + 1
        self.users.append(user)
        return user

    def update(self, id, data):
        user = self.get(id)
        user.update(data)
        return user

    def delete(self, id):
        user = self.get(id)
        self.users.remove(user)


class BorrowDao(object):
    def __init__(self):
        self.counter = 0
        self.borrows = []

    def get(self, id):
        for borrow in self.borrows:
            if borrow['id'] == id:
                return borrow
        api.abort(404, "Borrow {} doesn't exist".format(id))

    def create(self, data):
        borrow = data
        borrow['id'] = self.counter = self.counter + 1
        self.borrows.append(borrow)
        return borrow

    def update(self, id, data):
        borrow = self.get(id)
        borrow.update(data)
        return borrow

    def delete(self, id):
        borrow = self.get(id)
        self.borrows.remove(borrow)


book_dao = BookDAO()
book_dao.create({'book_name': 'book1'})
book_dao.create({'book_name': 'book2'})
book_dao.create({'book_name': 'book3'})

user_dao = UserDAO()
user_dao.create({'username': 'user1'})
user_dao.create({'username': 'user2'})
user_dao.create({'username': 'user3'})

borrow_dao = BorrowDao()
borrow_dao.create({'book_id': 1, 'user_id': 1})
borrow_dao.create({'book_id': 2, 'user_id': 1})
borrow_dao.create({'book_id': 3, 'user_id': 2})


@ns_book.route('/books')
class BookStore(Resource):
    @ns_book.marshal_list_with(books)
    def get(self):
        '''
        Check all books in the library.
        :rtype: List\<BookDAO\>
        '''
        return book_dao.books

    def post(self):
        '''
        Create a new book into the library.
        :rtype: BookDAO
        '''
        return book_dao.create({'book_name': 'new book'}), 201


@ns_book.route('/book/<int:id>')
class Book(Resource):
    def get(self, id):
        '''
        Check the book's info from the library.
        :param id: book's id
        :return: book's info
        :rtype: BookDAO
        '''
        return book_dao.get(id)

    def delete(self, id):
        '''
        Delete a book given its identifier
        :param id: book's id
        :return: None
        :rtype: None
        '''
        book_dao.delete(id)
        return '', 204

    def put(self, id):
        '''
        Update a book given its identifier
        :param id: book's id
        :return: book's updated info
        :rtype: BookDAO
        '''
        return book_dao.update(id, {'book_name': 'new book name'})


@ns_user.route('/users')
class UserList(Resource):
    @ns_user.marshal_list_with(users)
    def get(self):
        '''
        Check all users in the user list.
        :rtype: List\<UserDAO\>
        '''
        return user_dao.users

    def post(self):
        '''
        Create a new user into the user list.
        :rtype: UserDAO
        '''
        return user_dao.create({'username': 'new user'}), 201


@ns_user.route('/user/<int:id>')
class User(Resource):
    def get(self, id):
        '''
        Check the user's info from the user list.
        :param id: user's id
        :return: user's info
        :rtype: UserDAO
        '''
        return user_dao.get(id)

    def delete(self, id):
        '''
        Delete a user given its identifier
        :param id: user's id
        :return: None
        :rtype: None
        '''
        user_dao.delete(id)
        return '', 204

    def put(self, id):
        '''
        Update a user given its identifier
        :param id: user's id
        :return: user's updated info
        :rtype: UserDAO
        '''
        return user_dao.update(id, {'username': 'new username'})


@ns_borrow.route('/borrows')
class BorrowList(Resource):
    @ns_borrow.marshal_list_with(borrows)
    def get(self):
        '''
        Check all borrows in the library.
        :rtype: List\<BorrowDAO\>
        '''
        return borrow_dao.borrows

    def post(self):
        '''
        Create a new borrow into the library.
        :rtype: BorrowDAO
        '''
        return borrow_dao.create(api.payload), 201


@ns_borrow.route('/borrow/<int:id>')
class Borrow(Resource):
    def get(self, id):
        '''
        Check the borrow's info from the library.
        :param id: borrow's id
        :return: borrow's info
        :rtype: BorrowDAO
        '''
        return borrow_dao.get(id)

    def delete(self, id):
        '''
        Delete a borrow given its identifier
        :param id: borrow's id
        :return: None
        :rtype: None
        '''
        borrow_dao.delete(id)
        return '', 204

    def put(self, id):
        '''
        Update a borrow given its identifier
        :param id: borrow's id
        :return: borrow's updated info
        :rtype: BorrowDAO
        '''
        return borrow_dao.update(id, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
