from flask import Flask, render_template, url_for

app = Flask(__name__)

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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/bookstore')
def list_all_books():
    return render_template('bookstore.html', book_list=book_list)


@app.route('/book/<int:book_id>')
def show_book(book_id):
    book = None
    for book_item in book_list:
        if book_item['id'] == book_id:
            book = book_item
    return render_template('book.html', book=book)


@app.route('/user/<int:user_id>')
def show_user(user_id):
    return 'User ID is %d' % user_id


if __name__ == '__main__':
    app.run(debug=True)
