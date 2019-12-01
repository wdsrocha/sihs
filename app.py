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
from functools import wraps
from flask import send_file
import smtplib
from email.message import EmailMessage
import json

app = Flask(__name__)

from sqlalchemy import create_engine
engine = create_engine('postgres://postgres:123@localhost:5432/db_flask')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:123@localhost:5432/db_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
CORS(app,origins='*')

db = SQLAlchemy(app)

#DATABASE
class User(db.Model):
    __tablename__ = 'tbl_user'
    
    id = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(100),unique=True,nullable=False)
    device_id = db.Column(db.String(200),db.ForeignKey('tbl_device.id'),nullable=False) 

    invitation = db.relationship('Invitation')
    
    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"

    

class Device(db.Model):
    __tablename__ = 'tbl_device'

    id = db.Column(db.String(200), primary_key=True)
    
    
    users = db.relationship('User')
    
   
    def __repr__(self):
        return f"Device('{self.id}')"


class Invitation(db.Model):
    __tablename__ = 'tbl_invitation'
    
    id = db.Column(db.String(200), primary_key=True)
    qrcode=db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200), nullable=False)
    creation_date= db.Column(DateTime, default=datetime.datetime.utcnow)
    usage_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)

    user_id = db.Column(db.String(200),db.ForeignKey('tbl_user.id'), nullable=False)

    
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
    if(db.session.query(User.username).filter_by(username=data['username']).scalar() is not None):
        return 'This username already exist!'

    new_user=User(id=data['telegram_id'],username=data['username'],device_id=data['device_serial'])
    db.session.add(new_user)
    db.session.commit()
    response = make_response(jsonify({'message': 'User registred sucessfuly', 'username':new_user.username}))
    return response

## Get devices
@app.route('/devices')
def get_devices():
    devices = Device.query.all()
    print(devices)
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
    content = '{"user_id": "%s", "guest_email": "%s"}' % (data['user_id'], data['guest_email'])
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image()
    img.save("image.jpg")

    #send qrcode to email

    # if(db.session.query(Invitation.id).filter_by(id=data['id']).scalar() is not None):
    #      return 'This invitation already exist'

    new_invitation=Invitation(id=secrets.token_hex(16),qrcode=data['user_id']+data['guest_email'],user_id=data['user_id'],email=data['guest_email'], status='unused')
    db.session.add(new_invitation)
    db.session.commit()
    response = make_response(jsonify({'message': 'Invitaion created!', 'qrcode':new_invitation.qrcode}))
    return response


## Confirm code
@app.route('/confirm', methods=['POST'])
def confirm():
    data = request.get_json()
    
    qrcode_compact = data['user_id'] + data['guest_email']
    response = 'nothing'
    if(User.query.filter_by(id=data['user_id']).scalar() is not None):
        qrcode_invitation = Invitation.query.filter_by(qrcode=qrcode_compact).first()
        if qrcode_invitation is not None and qrcode_invitation.status == 'unused':
            qrcode_invitation.status = 'used'
            qrcode_invitation.usage_data = datetime.datetime.utcnow
            db.session.commit()
            response = make_response(jsonify({'message': 'Ok'}))
        else:
            response = make_response(jsonify({'message': 'Invalid invitation 1'}))
    else:
        response = make_response(jsonify({'message': 'Invalid invitation 2'}))
    
    return response
@app.route('/report', methods=['GET'])
def report():
    data = request.get_json()
    invitations = Invitation.query.filter_by(user_id=data['user_id'])
    output = []
    for i in invitations:
        data = {
            'email': i.email,
            'status': i.status,
            'creation_date': i.creation_date,
            'usage_date': i.usage_date
        }
        output.append(data)
    response = jsonify({"invitations": output})
    return response










