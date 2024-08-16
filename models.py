from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

class TransportDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transporter_name = db.Column(db.String(100))
    cheque_prepared_for = db.Column(db.String(100))
    received_date = db.Column(db.String(100))
    appointment_date = db.Column(db.String(100))
    goods_transported = db.Column(db.String(100))
    phone_no = db.Column(db.String(15))
    adr_koti = db.Column(db.String(200))
    gate_pass = db.Column(db.String(200))
    we_bill = db.Column(db.String(200))
    merchandise_receipt = db.Column(db.String(200))
    livery = db.Column(db.String(200))
    id_passport = db.Column(db.String(200))
    representation_letter = db.Column(db.String(200))
    dp_world = db.Column(db.String(200))
    association_receipt = db.Column(db.String(200))

if __name__ == "__main__":
    db.create_all()
