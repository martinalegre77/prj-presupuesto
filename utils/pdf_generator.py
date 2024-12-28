# Generación de PDFs.

from fpdf import FPDF

def generate_pdf(data, file_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=data, ln=True)
    pdf.output(file_name)
