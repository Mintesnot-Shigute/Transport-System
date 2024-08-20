from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, make_response
from models import db, TransportDocument
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'supersecretkey'

db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Ensure the uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def save_file(file, prefix=None):
    filename = secure_filename(file.filename)
    if prefix:
        # Extract file extension
        name, ext = os.path.splitext(filename)
        filename = f"{prefix}_{name}{ext}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return filename

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

@app.route('/', methods=['GET', 'POST'])
def claim():
    if request.method == 'POST':
        # Process quiz answers if needed
        return redirect(url_for('form'))  # Redirect to success page after quiz submission

    return render_template('transport_claim_form.html')



@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        transporter_name = request.form["transporter_name"]
        cheque_prepared_for = request.form["cheque_prepared_for"]
        received_date = request.form["received_date"]
        appointment_date = request.form["appointment_date"]
        goods_transported = request.form["goods_transported"]
        phone_no = request.form["phone_no"]

        credit_recipt = save_file(request.files['credit_recipt'], prefix=transporter_name) if 'credit_recipt' in request.files else None
        transport_agreement = save_file(request.files['transport_agreement'], prefix=transporter_name) if 'transport_agreement' in request.files else None
        way_bill = save_file(request.files['way_bill'], prefix=transporter_name) if 'way_bill' in request.files else None
        weight_scale = save_file(request.files['weight_scale'], prefix=transporter_name) if 'weight_scale' in request.files else None
        container_inspection = save_file(request.files['container_inspection'], prefix=transporter_name) if 'container_inspection' in request.files else None
        container_interchange = save_file(request.files['container_interchange'], prefix=transporter_name) if 'container_interchange' in request.files else None
        grn = save_file(request.files['grn'], prefix=transporter_name) if 'grn' in request.files else None
        libre = save_file(request.files['libre'], prefix=transporter_name) if 'libre' in request.files else None
        id_card = save_file(request.files['id_card'], prefix=transporter_name) if 'id_card' in request.files else None
        delegation_document = save_file(request.files['delegation_document'], prefix=transporter_name) if 'delegation_document' in request.files else None
        if None in [credit_recipt, transport_agreement, way_bill, weight_scale, container_inspection, container_interchange, grn, libre, id_card,delegation_document]:
            flash("Please upload all required documents.")
            return redirect(url_for('form'))

        new_document = TransportDocument(
            transporter_name=transporter_name,
            cheque_prepared_for=cheque_prepared_for,
            received_date=received_date,
            appointment_date=appointment_date,
            goods_transported=goods_transported,
            phone_no=phone_no,
            credit_recipt=credit_recipt,
            transport_agreement=transport_agreement,
            way_bill=way_bill,
            weight_scale=weight_scale,
            container_inspection=container_inspection,
            container_interchange=container_interchange,
            grn=grn,
            libre=libre,
            id_card=id_card,
            delegation_document=delegation_document
        )

        db.session.add(new_document)
        db.session.commit()

        flash("All documents uploaded successfully! Appointment date form generated.")
        return redirect(url_for('confirmation', document_id=new_document.id))

    return render_template("form.html")



@app.route("/confirmation/<int:document_id>")
def confirmation(document_id):
    document = TransportDocument.query.get_or_404(document_id)
    return render_template("confirmation.html", document=document)

@app.route("/download_pdf/<int:document_id>")
def download_pdf(document_id):
    document = TransportDocument.query.get_or_404(document_id)
    pdf, pdf_name = generate_pdf(document)
    
    response = make_response(pdf.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={pdf_name}'
    
    return response

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
