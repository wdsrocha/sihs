from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: add whole db model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


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


if __name__ == "__main__":
    app.run(debug=True)
