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
    invitation = db.relationship('Invitation')
   
    def __repr__(self):
        return f"Device('{self.id}')"


class Guest(db.Model):
    __tablename__ = 'db_guest'

    id = db.Column(db.String(200), primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    
    invitation = db.relationship('Invitation')
    
    def __repr__(self):
        return f"Guest('{self.email}', '{self.id}')"

class Invitation(db.Model):
    __tablename__ = 'db_invitaion'
    
    id = db.Column(db.String(200), primary_key=True)
    qrcode=db.Column(db.String(200),nullable=False)
    creation_date= db.Column(DateTime, default=datetime.datetime.utcnow)
    usage_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    user_id=db.Column(db.String(200),db.ForeignKey('db_users.id'), nullable=False)
    guest_id=db.Column(db.String(200),db.ForeignKey('db_guest.id'), nullable=False)
    device_id=db.Column(db.String(200),db.ForeignKey('db_device.id'),nullable=False)
    
    def __repr__(self):
        return f"Invitation('{self.qrcode}', '{self.id}')"




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

## Guest register 
@app.route('/guest',methods=['POST'] )
def registerGuest():
    data= request.get_json()
    if(db.session.query(Guest.email).filter_by(email=data['email']).scalar() is not None):
        return 'This guest is already registred'

    new_guest=Guest(id=data['id'],email=data['email'])
    db.session.add(new_guest)
    db.session.commit()
    response = make_response(jsonify({'message': 'Guest registred sucessfuly', 'username':new_guest.email}))
    return response

## Generate an invitation
@app.route('/invite',methods=['POST'])

def createInvitation():
    data = request.get_json()
    if(db.session.query(Invitation.id).filter_by(id=data['id']).scalar() is not None):
         return 'This invitation already exist'

    new_invitation=Invitation(id=data['id'],qrcode=generateQRImage(),user_id=data['user'],guest_id=data['guest'],device_id=data['device'])
    db.session.add(new_invitation)
    db.session.commit()
    response = make_response(jsonify({'message': 'Invitaion created!', 'qrcode':new_invitation.qrcode}))
    return response

## Get invitation
@app.route('/invitations')
def get_invitations():
    
    invitations= Invitation.query.all()
    output=[]
    for invitation in invitations:
        invitation_data ={"id":invitation.id,"qrcode":invitation.qrcode,"user":invitation.user_id,"guest":invitation.guest_id,"device":invitation.device_id}
        output.append(invitation_data)
        
    response = make_response(jsonify({'Invitations': output}))
    return response



## Generate qrcode
@app.route("/qrgenerator")
def generateQRImage():
    code = secrets.token_hex(16)
    url = pyqrcode.create(code)
    url.png('url.png', scale=8)
    print(url.terminal())
    return code
