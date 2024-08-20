from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the TransportDocument model
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

# Define the TransportClaim model
class TransportClaim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_location = db.Column(db.String(100))
    to_location = db.Column(db.String(100))
    paid_to = db.Column(db.String(100))
    plate_no = db.Column(db.String(100))
    types_of_product = db.Column(db.String(100))
    number_of_bags = db.Column(db.String(100))
    quintal = db.Column(db.String(100))
    unit_price = db.Column(db.String(100))
    total_price = db.Column(db.String(100))
    advance_payment = db.Column(db.String(100))
    remaining_payment = db.Column(db.String(100))
    remark = db.Column(db.Text)
    requested_by_name = db.Column(db.String(100))
    requested_by_signature = db.Column(db.String(100))
    requested_by_date = db.Column(db.String(100))
    approved_by_name = db.Column(db.String(100))
    approved_by_signature = db.Column(db.String(100))
    approved_by_date = db.Column(db.String(100))

# Create the tables in the database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
