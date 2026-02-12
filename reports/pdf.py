from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(data, response):
    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    doc.build([
        Paragraph("Rapport IA Fintech", styles["Title"]),
        Paragraph(data["recommendation"], styles["Normal"]),
    ])
