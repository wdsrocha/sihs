#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask import Flask, request,jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy #comunicacao com o banco
from random import randint
from sqlalchemy import DateTime
import qrcode
import pyqrcode
import datetime
from flask import send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost:5555/db_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app,origins='*')

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'db_users'
    
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    device_id = db.Column(db.Integer,db.ForeignKey('db_device.id'),nullable=False) 

    invitation = db.relationship('Invitation')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"
# insert into db_user values(11,'nat')

class Device(db.Model):
    __tablename__ = 'db_device'

    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(200), nullable=False)
    
    
    users = db.relationship('Users')
    invitation = db.relationship('Invitation')
   
    def __repr__(self):
        return f"Device('{self.serial}', '{self.id}')"
#insert into db_device values(1,'camera',1,2); 

class Guest(db.Model):
    __tablename__ = 'db_guest'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    
    invitation = db.relationship('Invitation')
    
    def __repr__(self):
        return f"Guest('{self.username}', '{self.id}')"
# insert into db_alloweduser values (3,'diogo','91c863584c871f224cd15215999b62c5',2)

class Invitation(db.Model):
    __tablename__ = 'db_invitaion'
    
    id = db.Column(db.Integer, primary_key=True)
    qrcode=db.Column(db.String(200),nullable=False)
    creation_date= db.Column(DateTime, default=datetime.datetime.utcnow)
    usage_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    user_id=db.Column(db.Integer,db.ForeignKey('db_users.id'), nullable=False)
    guest_id=db.Column(db.Integer,db.ForeignKey('db_guest.id'), nullable=False)
    device_id=db.Column(db.Integer,db.ForeignKey('db_device.id'),nullable=False)
    
    def __repr__(self):
        return f"Invitation('{self.username}', '{self.id}')"
#insert into db_event values(1,'festa',3,2)  

#routes
@app.route('/')
def main():
    return 'oi'

# User register 
@app.route('/register')
def registerUser():
    data= request.get_json()
    if(db.session.query(Users.id).filter_by(id=data['id']).scalar() is not None):
        return 'This user already exist'
    new_user=Users(username=data['username'],device_id=data['dispositivo'])
    db.session.add(new_user)
    db.session.commit()
    response = make_response(jsonify({'message': 'User registred sucessfuly', 'username':new_user.username}))
    return response

#get devices
@app.route('/devices/<int:device_id>')
def get_devices(devices_id):
    device=Device.query.filter_by(id=(device_id)).first()

    if(device ==  None):
        return 'No devices registered'
    output={
        'serial':device.serial
    }
    return jsonify(output)

#register guest
@app.route('/guest')
def registerGuest():
    data= request.get_json()
    if(db.session.query(Guest.email).filter_by(email=data['email']).scalar() is not None):
        return 'This user already exist'
    new_guest=Users(email=data['email'])
    db.session.add(new_guest)
    db.session.commit()
    response = make_response(jsonify({'message': 'User registred sucessfuly', 'username':new_user.username}))
    return response

#generate an invitation
@app.route('/invite')
def  get_invitation():
    data = request.get_json()
    if(db.session.query(Invitation.id).filter_by(id=data['id']).scalar() is not None):
        return 'This invitation already exist'
    new_invitation=Invitation(user_id=data['user_id'],guest_id=data['guest_id'],device_id=data['device_id'],qrcode=data['qrcode'])
    db.session.add(new_invitation)
    db.session.commit()
    response = make_response(jsonify({'message': 'Invitaion created!', 'qrcode':new_invitation.qrcode}))
    return response

@app.route("/qrgenerator")
def generateQRImage():
    link_to_post = "http://127.0.0.1:5000/"
    url = pyqrcode.create(link_to_post)
    url.png('url.png', scale=8)
    print(url.terminal())
    return 'Printing QR code'

@app.route('/validation/<validation_code>')
def validate_qrcode(validation_code):
    if(db.session.query(AllowedUser.id).filter_by(validation=validation_code).scalar() is not None):
        return 'False'
    return 'True'
    

# @app.route('/invitation', methods=['POST'])
# def invite_guest():
#     data = request.get_json()
#     if(db.session.query(AllowedUser.username).filter_by(username=data['name']).scalar() is not None):
#         return 'User ja cadastrado!'
#     new_user = AllowedUser(id = randint(0,100),username=data['name'],validation=data['validation_code'],user_id =data['user_id'])
#     db.session.add(new_user)
#     db.session.commit()
#     response = make_response(jsonify({'message': 'User Cadastrado!', 'id':new_user.id}))
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response

    