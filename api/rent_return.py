from flask import Response, jsonify
from flask_restplus import Namespace, Resource, reqparse
from models import *

api = Namespace('rent_return', description='RENT and RETURN operations')

parser = reqparse.RequestParser()
parser.add_argument('user_id', help='The user\'s id')
parser.add_argument('book_id', help='The book\'s id')
parser.add_argument('rent_date', help='The rent date of the book')
parser.add_argument('return_date', help='The return date of the book')


@api.route('')
class RentList(Resource):
    @api.doc('get all rent and return records')
    def get(self):
        '''
        Get all records.
        :rtype: List\<RentReturn\>
        '''
        query_record = RentReturn.query.all()
        response = [record.to_json() for record in query_record]
        return Response(json.dumps(response), mimetype='application/json', status=201)


@api.route('/<int:user_id>/<int:book_id>')
@api.param('user_id', 'The user identifier')
@api.param('book_id', 'The book identifier')
class Rent(Resource):
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
        rent_date = args['rent_date']

        new_record = RentReturn(user_id, book_id, rent_date)
        db.session.add(new_record)
        db.session.commit()
        return Response(new_record.to_json(), mimetype='application/json', status=201)

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
        return_date = args['return_date']
        record = RentReturn.query.filter_by(user_id=user_id).first()
        if record is None:
            return None, 404
        if return_date is not None:
            record.return_date = return_date
            record.status = 'RETURN'
        db.session.commit()
        data = json.dumps({'user_id': record.user_id, 'status': record.status,
                           'rent_date': record.rent_date, 'return_date': record.return_date},
                          default=datetime_handler)
        response = jsonify(data)
        response.status_code = 201
        return response
