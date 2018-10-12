from flask import Flask, render_template, url_for, jsonify
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

book_list = [
    {
        'id': 1,
        'author': 'Corey Schafer',
        'title': 'Book 1',
        'published_date': 'April 20, 2018'
    },
    {
        'id': 2,
        'author': 'Jane Doe',
        'title': 'Book 2',
        'published_date': 'April 21, 2018'
    }
]


@api.route('/books')
class BookStore(Resource):
    def get(Resource):
        return book_list

# @api.route('/book/<int:book_id>')
# def show_book(book_id):
#     book = None
#     for book_item in book_list:
#         if book_item['id'] == book_id:
#             book = book_item
#     return render_template('book.html', book=book)
#
#
# @api.route('/user/<int:user_id>')
# def show_user(user_id):
#     return 'User ID is %d' % user_id


if __name__ == '__main__':
    app.run(debug=True)
