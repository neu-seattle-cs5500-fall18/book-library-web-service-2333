from flask import Flask
from api import api
from models import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dbuser:dbpassword@mydb.cjmm694bjqke.us-west-1.rds.amazonaws.com/msd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jef940727,@localhost/msd'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

with app.app_context():
    db.create_all()

api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
