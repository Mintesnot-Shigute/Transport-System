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
    __tablename__ = 'transport_documents'  # Ensure this matches the actual table name
    id = db.Column(db.Integer, primary_key=True)
    transporter_name = db.Column(db.String(100), nullable=False)
    cheque_prepared_for = db.Column(db.String(100), nullable=False)
    received_date = db.Column(db.String(100), nullable=False)
    appointment_date = db.Column(db.String(100), nullable=False)
    goods_transported = db.Column(db.String(100), nullable=False)
    phone_no = db.Column(db.String(15), nullable=False)
    credit_recipt = db.Column(db.String(200))
    transport_agreement = db.Column(db.String(200))
    way_bill = db.Column(db.String(200))
    weight_scale = db.Column(db.String(200))
    container_inspection = db.Column(db.String(200))
    container_interchange = db.Column(db.String(200))
    grn = db.Column(db.String(200))
    libre = db.Column(db.String(200))
    id_card = db.Column(db.String(200))
    delegation_document = db.Column(db.String(200))

# Define the TransportClaim model
class TransportClaim(db.Model):
    __tablename__ = 'transport_claim'  # Explicitly define the table name
    id = db.Column(db.Integer, primary_key=True)
    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), nullable=False)
    paid_to = db.Column(db.String(100), nullable=False)
    plate_no = db.Column(db.String(100), nullable=False)
    types_of_product = db.Column(db.String(100), nullable=False)
    number_of_bags = db.Column(db.String(100), nullable=False)
    quintal = db.Column(db.String(100), nullable=False)
    unit_price = db.Column(db.String(100), nullable=False)
    total_price = db.Column(db.String(100), nullable=False)
    advance_payment = db.Column(db.String(100), nullable=False)
    remaining_payment = db.Column(db.String(100), nullable=False)
    remark = db.Column(db.Text)
    requested_by_name = db.Column(db.String(100), nullable=False)
    requested_by_signature = db.Column(db.String(100), nullable=False)
    requested_by_date = db.Column(db.String(100), nullable=False)
    approved_by_name = db.Column(db.String(100), nullable=False)
    approved_by_signature = db.Column(db.String(100), nullable=False)
    approved_by_date = db.Column(db.String(100), nullable=False)

# Create the tables in the database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
