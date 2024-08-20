from barcode import EAN13
from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Sample data (driver payment information)
driver_id = "123456789012"
payment_info = {
    "name": "John Doe",
    "amount": "$1000",
    "date": "2024-08-05"
}

# Generate the barcode
barcode = EAN13(driver_id, writer=ImageWriter())
barcode_path = f'{driver_id}.png'
barcode.save(barcode_path)

# Create a PDF with the barcode and payment details
pdf_path = f'{driver_id}_payment.pdf'
c = canvas.Canvas(pdf_path, pagesize=letter)
width, height = letter

# Add payment details
c.drawString(100, height - 100, f"Driver: {payment_info['name']}")
c.drawString(100, height - 120, f"Amount: {payment_info['amount']}")
c.drawString(100, height - 140, f"Date: {payment_info['date']}")

# Add the barcode image
c.drawImage(barcode_path, 100, height - 240, width=200, height=100)

# Save the PDF
c.save()

print(f"Barcode and payment details saved to {pdf_path}")




