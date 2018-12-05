from flask import Flask, send_from_directory
from api import api
from models import db
import os

app = Flask(__name__, static_folder='book-library/build')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dbuseruser:dbpassword@db4free.net/msdmsd'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

api.init_app(app)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("book-library/build/" + path):
        return send_from_directory('book-library/build', path)
    else:
        return send_from_directory('book-library/build', 'index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
