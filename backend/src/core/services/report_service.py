from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from core.models import Equipment, FileUpload
from django.db.models import Avg, Count

def generate_report(upload_id):
    """
    Generates a PDF report for the given upload_id.
    Returns: BytesIO buffer containing the PDF.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # 1. Title
    try:
        upload = FileUpload.objects.get(id=upload_id)
        filename = getattr(upload.file, 'name', 'Unknown File')
        uploaded_at = upload.uploaded_at.strftime("%Y-%m-%d %H:%M")
    except FileUpload.DoesNotExist:
        return None

    elements.append(Paragraph(f"Chemical Equipment Report", styles['Title']))
    elements.append(Paragraph(f"File: {filename}", styles['Normal']))
    elements.append(Paragraph(f"Uploaded: {uploaded_at}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # 2. Summary Statistics
    equipment = Equipment.objects.filter(file_upload_id=upload_id)
    total_count = equipment.count()
    if total_count == 0:
        elements.append(Paragraph("No equipment data found in this upload.", styles['Normal']))
        doc.build(elements)
        buffer.seek(0)
        return buffer

    averages = equipment.aggregate(
        avg_flow=Avg('flowrate'),
        avg_press=Avg('pressure'),
        avg_temp=Avg('temperature')
    )
    
    elements.append(Paragraph("Summary Statistics", styles['Heading2']))
    summary_data = [
        ["Metric", "Value"],
        ["Total Count", str(total_count)],
        ["Avg Flowrate", f"{averages['avg_flow']:.2f} m3/h"],
        ["Avg Pressure", f"{averages['avg_press']:.2f} atm"],
        ["Avg Temperature", f"{averages['avg_temp']:.2f} C"]
    ]
    
    summary_table = Table(summary_data, colWidths=[200, 200])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))

    # 3. Equipment List (First 20 items)
    elements.append(Paragraph("Equipment Data (Top 20)", styles['Heading2']))
    
    data = [["Name", "Type", "Flowrate", "Pressure", "Temp"]]
    for eq in equipment[:20]:
        data.append([
            eq.equipment_name,
            eq.equipment_type,
            f"{eq.flowrate:.1f}",
            f"{eq.pressure:.1f}",
            f"{eq.temperature:.1f}"
        ])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.aliceblue),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
