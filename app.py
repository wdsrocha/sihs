#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_cors import CORS
from flask import Flask, request,jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from random import randint
from sqlalchemy import DateTime
import qrcode
import pyqrcode
import datetime
import secrets
import png
from functools import wraps
from flask import send_file
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

from sqlalchemy import create_engine
engine = create_engine('postgres://postgres:123@localhost:5555/db_flask')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost:5555/db_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app,origins='*')

db = SQLAlchemy(app)

#DATABASE
class Users(db.Model):
    __tablename__ = 'db_users'
    
    id = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    device_id = db.Column(db.String(200),db.ForeignKey('db_device.id'),nullable=False) 

    invitation = db.relationship('Invitation')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"

    

class Device(db.Model):
    __tablename__ = 'db_device'

    id = db.Column(db.String(200), primary_key=True)
    
    
    users = db.relationship('Users')
    
   
    def __repr__(self):
        return f"Device('{self.id}')"


class Invitation(db.Model):
    __tablename__ = 'db_invitaion'
    
    id = db.Column(db.String(200), primary_key=True)
    qrcode=db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200), nullable=False)
    creation_date= db.Column(DateTime, default=datetime.datetime.utcnow)
    usage_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    user_id=db.Column(db.String(200),db.ForeignKey('db_users.id'), nullable=False)

    
    def __repr__(self):
        return f"Invitation('{self.email}','{self.qrcode}', '{self.id}')"




#ROUTES
@app.route('/')
def hello():
    return 'Hello'

## User register 
@app.route('/register',methods=['POST'])
def registerUser():
    data = request.get_json()
    if(db.session.query(Users.username).filter_by(username=data['username']).scalar() is not None):
        return 'This username already exist!'

    new_user=Users(id=data['id'],username=data['username'],device_id=data['dispositivo'])
    db.session.add(new_user)
    db.session.commit()
    response = make_response(jsonify({'message': 'User registred sucessfuly', 'username':new_user.username}))
    return response

## Get devices
@app.route('/devices')
def get_devices():
    devices= Device.query.all()
    output = []
    for device in devices:
        device_data = {'serial': device.id}

        output.append(device_data)
        
    response = make_response(jsonify({'Devices': output}))
    return response


## Generate an invitation
@app.route('/invite',methods=['POST'])
def createInvitation():
    #generate qrcode
    data = request.get_json()
    qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_H,
    box_size = 10,
    border = 4,
    )
    content = secrets.token_hex(16)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image()
    img.save("image.jpg")

    #send qrcode to email

    # if(db.session.query(Invitation.id).filter_by(id=data['id']).scalar() is not None):
    #      return 'This invitation already exist'

    new_invitation=Invitation(id=secrets.token_hex(16),qrcode=content,user_id=data['user'],email=data['email'])
    db.session.add(new_invitation)
    db.session.commit()
    response = make_response(jsonify({'message': 'Invitaion created!', 'qrcode':new_invitation.qrcode}))
    return response

