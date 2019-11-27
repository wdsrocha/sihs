#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask import Flask, request,jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy #comunicacao com o banco
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost:5555/db_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app,origins='*')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'db_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    password = db.Column(db.String(8),nullable=False)

    devices = db.relationship('Device')
    allowedusers = db.relationship('AllowedUser')
    events = db.relationship('Event')

    def __repr__(self):
        return f"User('{self.username}', '{self.id}', '{self.password}')"
# insert into db_user values(2,'nat','123')

class Device(db.Model):
    __tablename__ = 'db_device'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    
    
    id_user= db.Column(db.Integer,db.ForeignKey('db_user.id'), nullable=False)
   
    def __repr__(self):
        return f"Device('{self.name}', '{self.id}', '{self.status}')"
#insert into db_device values(1,'camera',1,2); 

class AllowedUser(db.Model):
    __tablename__ = 'db_alloweduser'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    validation=db.Column(db.String(100),nullable=False)
    
    user_id=db.Column(db.Integer,db.ForeignKey('db_user.id'), nullable=False)
    event = db.relationship('Event')
    
    def __repr__(self):
        return f"AllowedUser('{self.username}', '{self.id}')"
# insert into db_alloweduser values (3,'diogo','91c863584c871f224cd15215999b62c5',2)

class Event(db.Model):
    __tablename__ = 'db_event'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200),nullable=False)

    alloweds=db.Column(db.Integer,db.ForeignKey('db_alloweduser.id'), nullable=False)
    userid=db.Column(db.Integer,db.ForeignKey('db_user.id'), nullable=False)
    
    def __repr__(self):
        return f"Event('{self.username}', '{self.id}')"
#insert into db_event values(1,'festa',3,2)  

@app.route('/')
def main():
    return 'oi'

@app.route('/validator/<validation_code>')
def validate_qrcode(validation_code):
    if(db.session.query(AllowedUser.id).filter_by(validation=validation_code).scalar() is not None):
        return 'False'
    return 'True'

@app.route('/invitation', methods=['POST'])
def invite_guest():
    data = request.get_json()
    if(db.session.query(AllowedUser.username).filter_by(username=data['name']).scalar() is not None):
        return 'User ja cadastrado!'
    new_user = AllowedUser(id = randint(0,100),username=data['name'],validation=data['validation_code'],user_id =data['user_id'])
    db.session.add(new_user)
    db.session.commit()
    response = make_response(jsonify({'message': 'User Cadastrado!', 'id':new_user.id}))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

    