from os import path, sep
from flask import Flask
from web import db, ams

SQLITE_DB_URI = '%sdata.db'% (sep.join(path.dirname(path.realpath(__file__)).split(sep)[:-1])+sep)

app = Flask(__name__, static_folder='')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % SQLITE_DB_URI
app.config['SECRET_KEY'] = 'ce2c0c02d6d8413782794451788ffa7f'

db.init_app(app)

app.register_blueprint(ams)

if __name__ == '__main__':
    app.debug = 1
    app.run(host='127.0.0.1',port=1080)