from flask import Response, jsonify
from flask_restplus import Namespace, Resource, reqparse
from models import *

api = Namespace('users', description='USERS operations')

parser = reqparse.RequestParser()
parser.add_argument('username', help='The username of the user')
parser.add_argument('password', help='The password of the user')


@api.route('')
class UserList(Resource):
    @api.doc(responses={
        201: 'Success',
    })
    @api.doc('get all users')
    def get(self):
        '''
        Check all users in the user list.
        :rtype: List\<User\>
        '''
        query_record = User.query.all()
        response = [user.to_json() for user in query_record]
        return Response(json.dumps(response), mimetype='application/json', status=201)

    @api.doc(responses={
        201: 'Success',
    })
    @api.doc('create a new user')
    def post(self):
        '''
        Create a new user into the user list.
        :rtype: User
        '''
        args = parser.parse_args()
        username = args['username']
        password = args['password']

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()
        return Response(new_user.to_json(), mimetype='application/json', status=201)


@api.route('/<int:user_id>')
class UserIndividual(Resource):
    @api.doc(responses={
        201: 'Success',
        404: 'No such user'
    })
    @api.doc('get a user from its id')
    def get(self, user_id):
        '''
        Check the user's info from the user list.
        :param user_id: user's id
        :return: user's info
        :rtype: User
        '''
        user = User.query.filter_by(user_id=user_id).first()
        if user is not None:
            data = json.dumps({'user_id': user.user_id, 'username': user.username})
            response = jsonify(data)
            response.status_code = 201
            return response
        else:
            return None, 404

    @api.doc(responses={
        204: 'Success',
        404: 'No such user'
    })
    @api.doc('delete a user by its id')
    def delete(self, user_id):
        '''
        Delete a user given its identifier
        :param user_id: user's id
        :return: None
        :rtype: None
        '''
        user = User.query.filter_by(user_id=user_id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return None, 204
        else:
            return None, 404

    @api.doc(responses={
        201: 'Success',
        404: 'No such user'
    })
    @api.doc('update a user by its id')
    def put(self, user_id):
        '''
        Update a user given its identifier
        :param user_id: user's id
        :return: user's updated info
        :rtype: UserDAO
        '''
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            return None, 404
        if username is not None:
            user.username = username
        if password is not None:
            user.password = password
        db.session.commit()
        data = json.dumps({'user_id': user.user_id, 'username': user.username})
        response = jsonify(data)
        response.status_code = 201
        return response
