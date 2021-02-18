import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/test1'
db = SQLAlchemy(app)
# представим, что это данные, которые получили из таблиц
input_data = '{"str_id":"cEapjRt7HSZX7iO","name":"Инннннокентий","photo":"https://dl.airtable.com/.attachments/fa70928a82a214d22c4b7a2eeace79d2/e5a12360/2.jpg","methods":["Гештальт-терапия","Коучинг","Психосинтез","Сказкотерапия"]}'
map_data = json.loads(input_data)

class Psychotherapist(db.Model):
    def __init__(self, str_id, name, photo, methods):
        self.str_id = str_id
        self.name = name
        self.photo = photo
        self.methods = methods
    id = db.Column(db.Integer, primary_key=True)
    str_id = db.Column(db.String(20))
    name = db.Column(db.String(30))
    photo = db.Column(db.String)
    methods = db.Column(db.String)
    def __repr__(self):
        return self.str_id + ' ' + self.name + ' ' + self.photo + ' ' + self.methods

class Second_table(db.Model):
    def __init__(self, data):
        self.date = datetime.now()
        self.data = data
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    data = db.Column(db.String)
    def __repr__(self):
        return str(self.date) + ' ' + self.data

tmp = Second_table(input_data)
# если передавать массив словарей, то добавить for
el = Psychotherapist(map_data["str_id"],map_data["name"],map_data["photo"],map_data["methods"])
res = Psychotherapist.query.filter_by(str_id=el.str_id).first()
if res is None:
    db.session.add(el)
    db.session.add(tmp)
elif res.name != el.name:
    db.session.query(Psychotherapist).filter(Psychotherapist.str_id == el.str_id).\
    update({"name": el.name}, synchronize_session="fetch")
    db.session.add(tmp)
elif res.photo != el.photo:
    db.session.query(Psychotherapist).filter(Psychotherapist.str_id == el.str_id).\
    update({"photo": el.photo}, synchronize_session="fetch")
    db.session.add(tmp)
elif res.methods != el.methods:
    db.session.query(Psychotherapist).filter(Psychotherapist.str_id == el.str_id).\
    update({"methods": el.methods}, synchronize_session="fetch")
    db.session.add(tmp)

db.session.commit()

