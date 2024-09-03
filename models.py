from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the TransportRecord model
class TransportRecord(db.Model):
    __tablename__ = 'transport_records'
    
    # Fields from TransportDocument
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

    # Fields from TransportClaim
    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), nullable=False)
    paid_to = db.Column(db.String(100), nullable=False)
    plate_no = db.Column(db.String(50), nullable=False)
    types_of_product = db.Column(db.String(100), nullable=False)
    number_of_bags = db.Column(db.Integer, nullable=False)
    quintal = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    advance_payment = db.Column(db.Float, nullable=False)
    remaining_payment = db.Column(db.Float, nullable=False)
    remark = db.Column(db.String(200), nullable=True)
    requested_by_name = db.Column(db.String(100), nullable=False)
    requested_by_date = db.Column(db.String(50), nullable=False)
    can_be_rented = db.Column(db.String(3), nullable=True)  # Values will be "Yes" or "No"

    # Fields from Approval
    # Fields from Approval
    approver_name = db.Column(db.String(100), nullable=True)
    approved = db.Column(db.Boolean, default=False)  # Default to False
    approval_date = db.Column(db.String, nullable=True)
    status = db.Column(db.String(50), default='Waiting for Approval')  # New field
    def set_approval_status(self, approved: bool):
        self.approved = approved
        self.approval_date = datetime.now().date().strftime("%Y-%m-%d") if approved else None  # Store as a string in "YYYY-MM-DD" format
        self.status = 'Approved' if approved else 'Waiting for Approval'
        db.session.commit()
# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Create the tables in the database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
