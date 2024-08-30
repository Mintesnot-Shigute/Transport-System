from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, make_response
from flask_bcrypt import Bcrypt
from models import db, TransportDocument, TransportClaim, User  # Import User model
from functools import wraps
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'your_secret_key'

db.init_app(app)
bcrypt = Bcrypt(app)  # Initialize Bcrypt

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Ensure the uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to save files
def save_file(file, prefix=None):
    filename = secure_filename(file.filename)
    if prefix:
        name, ext = os.path.splitext(filename)
        filename = f"{prefix}_{name}{ext}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

# Function to generate PDF
def generate_pdf(document):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    # Set the title
    p.drawString(100, 750, "Transporter Details")

    # Transporter details
    p.drawString(100, 730, f"Transporter Name: {document.transporter_name}")
    p.drawString(100, 710, f"Cheque Prepared For: {document.cheque_prepared_for}")
    p.drawString(100, 690, f"Received Date: {document.received_date}")
    p.drawString(100, 670, f"Appointment Date: {document.appointment_date}")
    p.drawString(100, 650, f"Goods Transported: {document.goods_transported}")
    p.drawString(100, 630, f"Phone Number: {document.phone_no}")

    p.showPage()
    p.save()

    pdf_name = f"{document.transporter_name}_{document.appointment_date}_Appointment_Letter.pdf"
    buffer.seek(0)
    return buffer, pdf_name

# Function to protect routes based on roles
# Your role_required decorator
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash('Access denied.')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username_field')
        password = request.form.get('password_field')
        role = request.form.get('role')

        user = User.query.filter_by(username=username).first()
        if user and user.password == password and user.role == role:
            session['username'] = user.username
            session['role'] = user.role
            print(f"Session data: {session}")  # Debugging line
            if user.role == 'admin':
                return redirect(url_for('driver_list'))
            else:
                return redirect(url_for('claim'))
        else:
            flash('Invalid username, password, or role')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route to display transporter details
@app.route('/driver_list')
@role_required('admin')
def driver_list():
    documents = TransportDocument.query.all()
    claims = TransportClaim.query.all()
    
    return render_template('transportDetails.html', documents=documents, claims=claims)

@app.route('/claim', methods=['GET', 'POST'])
@role_required('user')
def claim():
    if request.method == 'POST':
        # Debugging: Print form data
        print("Form data:", request.form)
        
        # Extract data from form fields
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        paid_to = request.form.get('paid_to')
        plate_no = request.form.get('plate_no')
        types_of_product = request.form.get('types_of_product')
        number_of_bags = request.form.get('number_of_bags')
        quintal = request.form.get('quintal')
        unit_price = request.form.get('unit_price')
        total_price = request.form.get('total_price')
        advance_payment = request.form.get('advance_payment')
        remaining_payment = request.form.get('remaining_payment')
        remark = request.form.get('remark')
        requested_by_name = request.form.get('requested_by_name')
        requested_by_signature = request.form.get('requested_by_signature')
        requested_by_date = request.form.get('requested_by_date')
        approved_by_name = request.form.get('approved_by_name')
        approved_by_signature = request.form.get('approved_by_signature')
        approved_by_date = request.form.get('approved_by_date')
        can_be_rented = request.form.get('can_be_rented')  # Added field

        # Debugging: Print extracted data
        print("Extracted data:", {
            'from_location': from_location,
            'to_location': to_location,
            'paid_to': paid_to,
            'plate_no': plate_no,
            'types_of_product': types_of_product,
            'number_of_bags': number_of_bags,
            'quintal': quintal,
            'unit_price': unit_price,
            'total_price': total_price,
            'advance_payment': advance_payment,
            'remaining_payment': remaining_payment,
            'remark': remark,
            'requested_by_name': requested_by_name,
            'requested_by_signature': requested_by_signature,
            'requested_by_date': requested_by_date,
            'approved_by_name': approved_by_name,
            'approved_by_signature': approved_by_signature,
            'approved_by_date': approved_by_date,
            'can_be_rented': can_be_rented
        })

        # Create a new TransportClaim object
        new_claim = TransportClaim(
            from_location=from_location,
            to_location=to_location,
            paid_to=paid_to,
            plate_no=plate_no,
            types_of_product=types_of_product,
            number_of_bags=number_of_bags,
            quintal=quintal,
            unit_price=unit_price,
            total_price=total_price,
            advance_payment=advance_payment,
            remaining_payment=remaining_payment,
            remark=remark,
            requested_by_name=requested_by_name,
            requested_by_signature=requested_by_signature,
            requested_by_date=requested_by_date,
            approved_by_name=approved_by_name,
            approved_by_signature=approved_by_signature,
            approved_by_date=approved_by_date,
            can_be_rented=can_be_rented  # Added field
        )

        # Add and commit the new claim to the database
        db.session.add(new_claim)
        db.session.commit()

        # Debugging: Confirm successful commit
        print("New claim added and committed to database.")

        return redirect(url_for('form'))
    claims = TransportClaim.query.all()
    return render_template('transport_claim_form.html', claims=claims)


# Route for transporter form
@app.route("/form", methods=["GET", "POST"])
@role_required('user')  # Only accessible by User
def form():
    if request.method == "POST":
        transporter_name = request.form["transporter_name"]
        cheque_prepared_for = request.form["cheque_prepared_for"]
        received_date = request.form["received_date"]
        appointment_date = request.form["appointment_date"]
        goods_transported = request.form["goods_transported"]
        phone_no = request.form["phone_no"]

        # Define required documents
        required_documents = [
            'credit_recipt', 
            'transport_agreement', 
            'way_bill', 
            'weight_scale', 
            'container_inspection', 
            'grn', 
            'libre', 
            'id_card', 
            'delegation_document'
        ]
        
        # Track if all required documents are uploaded
        all_required_documents_uploaded = True
        
        # Handle file uploads
        uploaded_files = {}
        for doc in required_documents:
            if doc in request.files:
                uploaded_files[doc] = save_file(request.files[doc], prefix=transporter_name)
                if not uploaded_files[doc]:  # Check if file was saved successfully
                    all_required_documents_uploaded = False
            else:
                # Mark as not uploaded if it's a required document
                all_required_documents_uploaded = False

        if not all_required_documents_uploaded:
            flash("Please upload all required documents.")
            return redirect(url_for('form'))

        # Create a new TransportDocument object with uploaded files
        new_document = TransportDocument(
            transporter_name=transporter_name,
            cheque_prepared_for=cheque_prepared_for,
            received_date=received_date,
            appointment_date=appointment_date,
            goods_transported=goods_transported,
            phone_no=phone_no,
            credit_recipt=uploaded_files.get('credit_recipt'),
            transport_agreement=uploaded_files.get('transport_agreement'),
            way_bill=uploaded_files.get('way_bill'),
            weight_scale=uploaded_files.get('weight_scale'),
            container_inspection=uploaded_files.get('container_inspection'),
            container_interchange=uploaded_files.get('container_interchange'),
            grn=uploaded_files.get('grn'),
            libre=uploaded_files.get('libre'),
            id_card=uploaded_files.get('id_card'),
            delegation_document=uploaded_files.get('delegation_document')
        )

        # Add and commit the new document to the database
        db.session.add(new_document)
        db.session.commit()

        flash("All documents uploaded successfully!")
        return redirect(url_for('confirmation', document_id=new_document.id))



    return render_template("form.html")


# Route for confirmation page
@app.route("/confirmation/<int:document_id>")
@role_required('user')  # Only accessible by Admin
def confirmation(document_id):
    document = TransportDocument.query.get_or_404(document_id)
    return render_template("confirmation.html", document=document)

# Route to download PDF
@app.route("/download_pdf/<int:document_id>")
def download_pdf(document_id):
    document = TransportDocument.query.get_or_404(document_id)
    pdf, pdf_name = generate_pdf(document)

    response = make_response(pdf.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={pdf_name}'

    return response

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to log out the user
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
