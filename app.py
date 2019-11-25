#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask import Flask, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy #comunicacao com o banco

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
    
    device_id = db.Column(db.Integer,db.ForeignKey('db_device.id'), nullable=False)
    alloweduser_id=db.Column(db.Integer,db.ForeignKey('db_alloweduser.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.id}', '{self.password}')"

class Device(db.Model):
    __tablename__ = 'db_device'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    
    users = db.relationship('User')
    
    def __repr__(self):
        return f"Device('{self.name}', '{self.id}', '{self.status}')"
   
class AllowedUser(db.Model):
    __tablename__ = 'db_alloweduser'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    allowedusers = db.relationship('User')
    event = db.relationship('Event')
    def __repr__(self):
        return f"AllowedUser('{self.username}', '{self.id}')"

class Event(db.Model):
    __tablename__ = 'db_event'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200),nullable=False)

    alloweds=db.Column(db.Integer,db.ForeignKey('db_alloweduser.id'), nullable=False)
    
    events = db.relationship('User')
    
    def __repr__(self):
        return f"Event('{self.username}', '{self.id}')"

@app.route('/')
def main():
    return 'aaaa'

@app.route('/validation')
def validate_qrcode():
    # TODO: assert request.args is { "qrcode": "string here" }
    # TODO: notify user that guest had access, if qrcode is valid
    # TODO: tell device to grant access to guest, if qrcode is valid
    return jsonify(request.args)


@app.route('/invitation', methods=['POST'])
def invite_guest():
    # TODO: think about the logic here and implement :v
    return jsonify(request.json)