#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import secrets
import smtplib
from email.message import EmailMessage

import qrcode
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
import imghdr

app = Flask(__name__)


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgres://postgres:123@localhost:5555/db_flask"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
CORS(app, origins="*")

db = SQLAlchemy(app)


# DATABASE
class User(db.Model):
    __tablename__ = "tbl_user"

    id = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    device_id = db.Column(
        db.String(200), db.ForeignKey("tbl_device.id"), nullable=False
    )

    invitation = db.relationship("Invitation")

    def __repr__(self):
        return f"User('{self.username}', '{self.id}')"


class Device(db.Model):
    __tablename__ = "tbl_device"

    id = db.Column(db.String(200), primary_key=True)

    users = db.relationship("User")

    def __repr__(self):
        return f"Device('{self.id}')"


class Invitation(db.Model):
    __tablename__ = "tbl_invitation"

    id = db.Column(db.String(200), primary_key=True)
    qrcode = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    creation_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    usage_date = db.Column(DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), nullable=False)
    count_error = db.Column(db.Integer(), default=0)
    user_id = db.Column(db.String(200), db.ForeignKey("tbl_user.id"), nullable=False)

    def __repr__(self):
        return f"Invitation('{self.email}','{self.qrcode}', '{self.id}')"


# ROUTES
@app.route("/")
def hello():
    return "Hello"


## User register
@app.route("/register", methods=["POST"])
def registerUser():
    data = request.get_json()
    if (
        db.session.query(User.username).filter_by(username=data["username"]).scalar()
        is not None
    ):
        return "This username already exist!"

    new_user = User(
        id=data["telegram_id"],
        username=data["username"],
        device_id=data["device_serial"],
    )
    db.session.add(new_user)
    db.session.commit()
    response = make_response(
        jsonify({"message": "User registred sucessfuly", "username": new_user.username})
    )
    return response


## Get devices
@app.route("/devices")
def get_devices():
    devices = Device.query.all()
    print(devices)
    output = []
    for device in devices:
        device_data = {"serial": device.id}

        output.append(device_data)

    response = make_response(jsonify({"Devices": output}))
    return response


@app.route("/users")
def get_users():
    users = User.query.all()
    output = []
    for u in users:
        user_data = {
            "username": u.username,
            "device": u.device_id
        }
        output.append(user_data)

    response = make_response(jsonify({"Users": output}))
    return response


## Generate an invitation
@app.route("/invite", methods=["POST"])
def createInvitation():
    # generate qrcode
    data = request.get_json()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    content = '{"user_id": "%s", "guest_email": "%s"}' % (
        data["user_id"],
        data["guest_email"],
    )
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image()
    
    img_path = "images/"+data["user_id"] + data["guest_email"]+".jpg"
    img.save(img_path)

    # send qrcode to email
    EMAIL_ADDRESS = "nataliacxavier1@gmail.com"  # put email here
    EMAIL_PASSWORD = "***REMOVED***"  # password here
    msg = EmailMessage()
    msg["Subject"] = "Hey you!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = data["guest_email"]
    msg.set_content("Come to see me, you only have to use this qrcode")


    with open(img_path, "rb") as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name
    msg.add_attachment(
        file_data, maintype="image", subtype=file_type, filename=file_name
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    new_invitation = Invitation(
        id=secrets.token_hex(16),
        qrcode=data["user_id"] + data["guest_email"],
        user_id=data["user_id"],
        email=data["guest_email"],
        status="unused",
    )

    db.session.add(new_invitation)
    db.session.commit()
    response = make_response(
        jsonify({"message": "Invitaion created!", "qrcode": new_invitation.qrcode})
    )
    return response


## Confirm code
@app.route("/confirm", methods=["POST"])
def confirm():
    data = request.get_json()

    qrcode_compact = data["user_id"] + data["guest_email"]
    response = "nothing"
    if User.query.filter_by(id=data["user_id"]).scalar() is not None:
        qrcode_invitation = Invitation.query.filter_by(qrcode=qrcode_compact).first()
        if qrcode_invitation is not None and qrcode_invitation.status == "unused":
            qrcode_invitation.status = "used"
            qrcode_invitation.usage_data = datetime.datetime.utcnow
            db.session.commit()
            response = make_response(jsonify({"message": "Ok"}))
        else:
            if qrcode_invitation.status == 'used':
                qrcode_invitation.count_error = qrcode_invitation.count_error + 1
                print("erros->", qrcode_invitation.count_error)
                db.session.commit()
            response = make_response(jsonify({"message": "Invalid invitation 1"}))
    else:
        response = make_response(jsonify({"message": "Invalid invitation 2"}))

    return response


@app.route("/report", methods=["GET"])
def report():
    data = request.get_json()
    invitations = Invitation.query.filter_by(user_id=data["user_id"])
    output = []
    for i in invitations:
        data = {
            "email": i.email,
            "status": i.status,
            "creation_date": i.creation_date,
            "usage_date": i.usage_date,
        }
        output.append(data)
    response = jsonify({"invitations": output})
    return response

@app.route("/report-access", methods=["GET"])
def report_access():
    data = request.get_json()
    invitations = Invitation.query.filter_by(user_id=data["user_id"])
    freq_month = []
    
    for i in range(0,13):
        freq_month.append(0)

    for i in invitations:
        freq_month[i.usage_date.month] += 1
    
    response = jsonify({"freq_month": freq_month})
    return response

@app.route("/report-access-positive", methods=["GET"])
def report_access_positive():
    data = request.get_json()
    invitations = Invitation.query.filter_by(user_id=data["user_id"])
    freq_month = []
    
    for i in range(0,13):
        freq_month.append(0)

    for i in invitations:
        if i.status == 'used':
            freq_month[i.usage_date.month] += 1
    
    response = jsonify({"freq_month": freq_month})
    return response

    
@app.route("/report-access-negative", methods=["GET"])
def report_access_negative():
    data = request.get_json()
    invitations = Invitation.query.filter_by(user_id=data["user_id"])
    freq_month = []
    
    for i in range(0,13):
        freq_month.append(0)

    for i in invitations:
        freq_month[i.usage_date.month] += i.count_error
        print("errors:", freq_month[i.usage_date.month])
    
    response = jsonify({"freq_month": freq_month})
    return response


