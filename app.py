from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, make_response

from models import db, TransportRecord, User  # Import User model
from functools import wraps
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
from flask import request, render_template
from sqlalchemy import and_


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
            if user.role == 'superadmin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('userDashboard'))
        else:
            flash('Invalid username, password, or role')
            return redirect(url_for('login'))

    return render_template('login.html')

# Route to display transporter details
@app.route('/driver_list', methods=['GET'])
@role_required('admin')
def driver_list():
    # Get filter parameters from the query string
    status_filter = request.args.get('status')
    date_filter = request.args.get('date_filter')
    reference_filter = request.args.get('reference')  # New filter for reference number
    action = request.args.get('action')  # Action to determine which button was pressed

    # Start with the base query
    query = TransportRecord.query

    # Apply filters based on the button pressed
    if action == 'filter':
        # Apply status filter if provided
        if status_filter in ['Approved', 'Waiting for Approval']:
            query = query.filter(TransportRecord.status == status_filter)

        # Apply date filter if provided
        if date_filter == 'upcoming':
            today = datetime.today().date()
            future_date = today + timedelta(days=10)
            query = query.filter(and_(TransportRecord.appointment_date >= today,
                                      TransportRecord.appointment_date <= future_date))
        elif date_filter == 'past':
            today = datetime.today().date()
            query = query.filter(TransportRecord.appointment_date < today)

    elif action == 'search':
        # Apply reference number filter if provided
        if reference_filter:
            query = query.filter(TransportRecord.reference.like(f'%{reference_filter}%'))

    # Fetch the filtered records
    documents = query.all()

    # Render the template with the filtered documents
    return render_template('transportDetails.html', documents=documents)

@app.route('/userDashboard')
@role_required('user')
def userDashboard():
    return render_template('userDashboard.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Collect form data
        transporter_name = request.form.get('transporter_name')
        cheque_prepared_for = request.form.get('cheque_prepared_for')
        received_date = request.form.get('received_date')
        appointment_date = request.form.get('appointment_date')
        goods_transported = request.form.get('goods_transported')
        phone_no = request.form.get('phone_no')

        # Transport Claim Fields
        from_location = request.form.get('from_location')
        to_location = request.form.get('to_location')
        paid_to = request.form.get('paid_to')
        plate_no = request.form.get('plate_no')
        types_of_product = request.form.get('types_of_product')
        can_be_rented = request.form.get('can_be_rented')
        number_of_bags = request.form.get('number_of_bags')
        quintal = request.form.get('quintal')
        unit_price = request.form.get('unit_price')
        total_price = request.form.get('total_price')
        advance_payment = request.form.get('advance_payment')
        remaining_payment = request.form.get('remaining_payment')
        requested_by_name = request.form.get('requested_by_name')
        requested_by_date = request.form.get('requested_by_date')
        remark = request.form.get('remark')

        # Handle file uploads
        uploaded_files = {
            'credit_recipt': request.files.get('credit_recipt'),
            'transport_agreement': request.files.get('transport_agreement'),
            'way_bill': request.files.get('way_bill'),
            'weight_scale': request.files.get('weight_scale'),
            'container_inspection': request.files.get('container_inspection'),
            'container_interchange': request.files.get('container_interchange'),
            'grn': request.files.get('grn'),
            'libre': request.files.get('libre'),
            'id_card': request.files.get('id_card'),
            'delegation_document': request.files.get('delegation_document'),
        }
        
        # Save files
        saved_files = {}
        for key, file in uploaded_files.items():
            if file and file.filename:
                filename = save_file(file, prefix=key)
                saved_files[key] = filename
        
        # Create a new transport document record
        new_document = TransportRecord(
            transporter_name=transporter_name,
            cheque_prepared_for=cheque_prepared_for,
            received_date=received_date,
            appointment_date=appointment_date,
            goods_transported=goods_transported,
            phone_no=phone_no,
            from_location=from_location,
            to_location=to_location,
            paid_to=paid_to,
            plate_no=plate_no,
            types_of_product=types_of_product,
            can_be_rented=can_be_rented,
            number_of_bags=int(number_of_bags),
            quintal=float(quintal),
            unit_price=float(unit_price) if unit_price else None,
            total_price=float(total_price) if total_price else None,
            advance_payment=float(advance_payment) if advance_payment else None,
            remaining_payment=float(remaining_payment) if remaining_payment else None,
            remark=remark,
            requested_by_name=requested_by_name,
            requested_by_date=requested_by_date,
            **saved_files
        )
        
        # Generate the reference number
        new_document.generate_reference()
        
        try:
            db.session.add(new_document)
            db.session.commit()
            # Redirect to the confirmation page with the document_id
            return redirect(url_for('confirmation', document_id=new_document.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}')

    return render_template('form.html')

# Route for confirmation page
@app.route("/confirmation")
@role_required('user')  # Only accessible by users with the 'user' role
def confirmation():
    # Get filter parameters from the query string
    status_filter = request.args.get('status')
    date_filter = request.args.get('date_filter')
    reference_filter = request.args.get('reference')  # New filter for reference number
    action = request.args.get('action')  # Action to determine which button was pressed

    # Start with the base query
    query = TransportRecord.query

    # Apply filters based on the button pressed
    if action == 'filter':
        # Apply status filter if provided
        if status_filter in ['Approved', 'Waiting for Approval']:
            query = query.filter(TransportRecord.status == status_filter)

        # Apply date filter if provided
        if date_filter == 'upcoming':
            today = datetime.today().date()
            future_date = today + timedelta(days=10)
            query = query.filter(and_(TransportRecord.appointment_date >= today,
                                      TransportRecord.appointment_date <= future_date))
        elif date_filter == 'past':
            today = datetime.today().date()
            query = query.filter(TransportRecord.appointment_date < today)

    elif action == 'search':
        # Apply reference number filter if provided
        if reference_filter:
            query = query.filter(TransportRecord.reference.like(f'%{reference_filter}%'))

    # Fetch the filtered records
    documents = query.all()

    # Render the template with the filtered documents
    return render_template('confirmation.html', documents=documents)


@app.route('/admin_dashboard', methods=['GET', 'POST'])
@role_required('superadmin')
def admin_dashboard():
    users = User.query.all()

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'create':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            new_user = User(username=username, password=password, role=role)
            
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('User created successfully!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Error: User could not be created.', 'danger')
            
        elif action == 'update':
            user_id = request.form['user_id']
            user = User.query.get_or_404(user_id)
            user.username = request.form['username']
            user.password = request.form['password']
            user.role = request.form['role']

            try:
                db.session.commit()
                flash('User updated successfully!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Error: User could not be updated.', 'danger')
        
        elif action == 'delete':
            user_id = request.form['user_id']
            user = User.query.get_or_404(user_id)
            try:
                db.session.delete(user)
                db.session.commit()
                flash('User deleted successfully!', 'success')
            except IntegrityError:
                db.session.rollback()
                flash('Error: User could not be deleted.', 'danger')

        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_dashboard.html', users=users)


@app.route('/approve/<int:record_id>', methods=['POST'])
def approve_record(record_id):
    record = TransportRecord.query.get_or_404(record_id)
    if record:
        record.set_approval_status(True)  # Set as approved
        record.approver_name = session.get('username', 'Unknown')  # Assuming username is stored in session
        db.session.commit()
    return redirect(url_for('driver_list'))

# Route to download PDF
@app.route("/download_pdf/<int:document_id>")
def download_pdf(document_id):
    document = TransportRecord.query.get_or_404(document_id)
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