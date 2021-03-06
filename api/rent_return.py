from flask import Response, jsonify
from flask_restplus import Namespace, Resource, reqparse
from models import *
from datetime import datetime

api = Namespace('rent_return', description='RENT and RETURN operations')

parser = reqparse.RequestParser()
parser.add_argument('user_id', help='The user\'s id')
parser.add_argument('book_id', help='The book\'s id')
parser.add_argument('rent_date', help='The rent date of the book')
parser.add_argument('return_date', help='The return date of the book')


@api.route('')
class RentList(Resource):
    @api.doc(responses={
        201: 'Success',
    })
    @api.doc('get all rent and return records')
    def get(self):
        '''
        Get all records.
        :rtype: List\<RentReturn\>
        '''
        query_record = RentReturn.query.all()
        response = [record.to_json() for record in query_record]
        return Response(json.dumps(response), mimetype='application/json', status=201)


@api.route('/<int:user_id>')
@api.param('user_id', 'The user identifier')
class RentUser(Resource):
    @api.doc(responses={
        201: 'Success',
    })
    @api.doc('get all books the user has not return')
    def get(self, user_id):
        """
        Get all books the user borrows and returns.
        :param user_id: user's id
        :return: a list of RentReturn record
        :rtype: List\<RentReturn\>
        """
        records = db.session.query(RentReturn, Book).filter(RentReturn.user_id == user_id).filter(
            RentReturn.book_id == Book.book_id).filter(RentReturn.status == 'RENT').all()
        response = [json.dumps({'book_id': book.book_id, 'book_name': book.book_name, 'author': book.author,
                                'genre': book.genre, 'rent_date': rent_return.rent_date},
                               default=datetime_handler) for rent_return, book
                    in records]
        return Response(json.dumps(response), mimetype='application/json', status=201)


@api.route('/<int:user_id>/<int:book_id>')
@api.param('user_id', 'The user identifier')
@api.param('book_id', 'The book identifier')
class RentBook(Resource):
    @api.doc(responses={
        201: 'Success',
        401: 'Book has been borrowed'
    })
    @api.doc('user borrows a book')
    def post(self, user_id, book_id):
        '''
        User borrows a book.
        :param user_id: user's id
        :param book_id: book's id
        :return: a RentReturn record
        :rtype: RentReturn
        '''
        args = parser.parse_args()
        date_string = datetime.fromtimestamp(int(args['rent_date']) / 1000).strftime(
            "%Y-%m-%d %H:%M:%S")
        rent_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

        book = Book.query.filter_by(book_id=book_id).first()
        if not book.available:
            return None, 401
        book.available = False

        new_record = RentReturn(user_id, book_id, rent_date)
        db.session.add(new_record)
        db.session.commit()
        return Response(new_record.to_json(), mimetype='application/json', status=201)

    @api.doc(responses={
        201: 'Success',
        401: 'User did not borrow the book',
        402: 'Invalid arguments'
    })
    @api.doc('user returns a book')
    def put(self, user_id, book_id):
        '''
        User returns a book.
        :param user_id: user's id
        :param book_id: book's id
        :return: a RentReturn record
        :rtype: RentReturn
        '''
        args = parser.parse_args()
        date_string = datetime.fromtimestamp(int(args['return_date']) / 1000).strftime(
            "%Y-%m-%d %H:%M:%S")
        return_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

        if return_date is None:
            return None, 402
        record = RentReturn.query.filter_by(user_id=user_id, book_id=book_id, return_date=None).first()
        if record is None:
            return None, 401
        record.return_date = return_date
        record.status = 'RETURN'
        book = Book.query.filter_by(book_id=book_id).first()
        book.available = True
        db.session.commit()
        data = json.dumps({'user_id': record.user_id, 'status': record.status,
                           'rent_date': record.rent_date, 'return_date': record.return_date},
                          default=datetime_handler)
        response = jsonify(data)
        response.status_code = 201
        return response
