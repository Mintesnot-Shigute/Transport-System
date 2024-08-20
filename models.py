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
    credit_recipt = db.Column(db.String(200))
    transport_agreement = db.Column(db.String(200))
    way_bill = db.Column(db.String(200))
    weight_scale = db.Column(db.String(200))
    container_inspection= db.Column(db.String(200))
    container_interchange = db.Column(db.String(200))
    grn= db.Column(db.String(200))
    libre = db.Column(db.String(200))
    id_card = db.Column(db.String(200))
    delegation_document = db.Column(db.String(200))

if __name__ == "__main__":
    db.create_all()
