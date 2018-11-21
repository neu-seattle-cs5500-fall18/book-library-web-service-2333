from flask_restplus import Api
from api.books import api as books_api
from api.users import api as users_api
from api.rent_return import api as rr_api

api = Api(version='1.0', title='Book Store API',
          description='A simple Book Store API')

api.add_namespace(books_api, path='/books')
api.add_namespace(users_api, path='/users')
api.add_namespace(rr_api, path='/rent_return')
