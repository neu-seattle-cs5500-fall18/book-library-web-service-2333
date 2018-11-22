from flask import Response, jsonify
from flask_restplus import Namespace, Resource, reqparse
from models import *

api = Namespace('books', description='BOOK operations')

parser = reqparse.RequestParser()
parser.add_argument('book_name', help='The name of the book')
parser.add_argument('author', help='The author of the book')
parser.add_argument('publish_date', help='The publish date of book')


@api.route('')
class BookStore(Resource):
    @api.doc(responses={
        201: 'Success',
    })
    @api.doc('get all books')
    def get(self):
        '''
        Check all books in the library.
        :rtype: List\<Book\>
        '''
        query_record = Book.query.all()
        response = [book.to_json() for book in query_record]
        return Response(json.dumps(response), mimetype='application/json', status=201)

    @api.doc(responses={
        201: 'Success',
    })
    @api.doc('create a new book')
    def post(self):
        '''
        Create a new book into the library.
        :rtype: Book
        '''
        args = parser.parse_args()
        book_name = args['book_name']
        author = args['author']
        publish_date = args['publish_date']

        new_book = Book(book_name, author, publish_date)
        db.session.add(new_book)
        db.session.commit()
        return Response(new_book.to_json(), mimetype='application/json', status=201)


@api.route('/<int:book_id>')
@api.param('book_id', 'The book identifier')
class BookIndividual(Resource):
    @api.doc(responses={
        201: 'Success',
        404: 'No such book'
    })
    @api.doc('get a book from its id')
    def get(self, book_id):
        '''
        Check the book's info from the library.
        :param book_id: book's id
        :return: book's info
        :rtype: Book
        '''
        book = Book.query.filter_by(book_id=book_id).first()
        if book is not None:
            data = json.dumps({'book_id': book.book_id, 'book_name': book.book_name, 'author': book.author,
                               'publish_date': book.publish_date, 'available': book.available},
                              default=datetime_handler)
            response = jsonify(data)
            response.status_code = 201
            return response
        else:
            return None, 404

    @api.doc(responses={
        204: 'Success',
        404: 'No such book'
    })
    @api.doc('delete a book by its id')
    def delete(self, book_id):
        '''
        Delete a book given its identifier
        :param book_id: book's id
        :return: None
        :rtype: None
        '''
        book = Book.query.filter_by(book_id=book_id).first()
        if book is not None:
            db.session.delete(book)
            db.session.commit()
            return None, 204
        else:
            return None, 404

    @api.doc(responses={
        201: 'Success',
        404: 'No such book'
    })
    @api.doc('update a book by its id')
    def put(self, book_id):
        '''
        Update a book given its identifier
        :param book_id: book's id
        :return: book's updated info
        :rtype: Book
        '''
        args = parser.parse_args()
        book_name = args['book_name']
        author = args['author']
        publish_date = args['publish_date']
        book = Book.query.filter_by(book_id=book_id).first()
        if book is None:
            return None, 404
        if book_name is not None:
            book.book_name = book_name
        if author is not None:
            book.author = author
        if publish_date is not None:
            book.publish_date = publish_date
        db.session.commit()
        data = json.dumps({'book_id': book.book_id, 'book_name': book.book_name, 'author': book.author,
                           'publish_date': book.publish_date, 'available': book.available}, default=datetime_handler)
        response = jsonify(data)
        response.status_code = 201
        return response
