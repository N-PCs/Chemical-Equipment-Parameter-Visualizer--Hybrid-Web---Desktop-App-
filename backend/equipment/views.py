"""
Equipment App - API Views
REST API endpoints for CSV upload, dataset history, and PDF generation.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, authentication
from django.http import HttpResponse
import pandas as pd
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch

from .models import Dataset


class EquipmentUploadView(APIView):
    """
    POST /api/upload/
    Upload CSV file, parse with Pandas, calculate summary, store in database.
    """
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response(
                {"error": "No file uploaded"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Parse CSV with Pandas
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            elif file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file)
            else:
                return Response(
                    {"error": "Unsupported file format. Use CSV, XLSX, or XLS."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate required columns
            required_cols = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            if not all(col in df.columns for col in required_cols):
                return Response(
                    {"error": f"Invalid schema. Required columns: {', '.join(required_cols)}"}, 
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            # Calculate summary statistics
            summary = {
                "total_count": len(df),
                "avg_flowrate": float(df['Flowrate'].mean()),
                "avg_pressure": float(df['Pressure'].mean()),
                "avg_temperature": float(df['Temperature'].mean()),
                "type_distribution": df['Type'].value_counts().to_dict()
            }
            
            # Prepare data for storage
            data_records = df.to_dict(orient='records')
            
            # Normalize column names for frontend (snake_case)
            normalized_data = []
            for record in data_records:
                normalized_data.append({
                    'equipment_name': record['Equipment Name'],
                    'type': record['Type'],
                    'flowrate': float(record['Flowrate']),
                    'pressure': float(record['Pressure']),
                    'temperature': float(record['Temperature'])
                })
            
            # Generate unique ID
            dataset_id = f"ds_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(file.name) % 10000}"
            
            # Save to database
            dataset = Dataset.objects.create(
                id=dataset_id,
                filename=file.name,
                total_count=summary['total_count'],
                avg_flowrate=summary['avg_flowrate'],
                avg_pressure=summary['avg_pressure'],
                avg_temperature=summary['avg_temperature'],
                type_distribution=summary['type_distribution'],
                data=normalized_data
            )
            
            # Maintain history limit (keep only last 5)
            Dataset.maintain_history_limit()
            
            return Response({
                "id": dataset.id,
                "filename": dataset.filename,
                "timestamp": dataset.uploaded_at.isoformat(),
                "summary": summary,
                "data": normalized_data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": f"Processing failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DatasetHistoryView(APIView):
    """
    GET /api/history/
    Returns metadata of the last 5 successful uploads.
    """
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            datasets = Dataset.objects.all()[:5]  # Already ordered by -uploaded_at
            
            history = []
            for dataset in datasets:
                history.append({
                    "id": dataset.id,
                    "filename": dataset.filename,
                    "timestamp": dataset.uploaded_at.isoformat(),
                    "summary": {
                        "total_count": dataset.total_count,
                        "avg_flowrate": dataset.avg_flowrate,
                        "avg_pressure": dataset.avg_pressure,
                        "avg_temperature": dataset.avg_temperature,
                        "type_distribution": dataset.type_distribution
                    },
                    "data": dataset.data
                })
            
            return Response(history, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"Failed to retrieve history: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GeneratePDFView(APIView):
    """
    POST /api/generate-pdf/
    Generate PDF report for a dataset.
    """
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            dataset_id = request.data.get('id')
            if not dataset_id:
                return Response(
                    {"error": "Dataset ID required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                dataset = Dataset.objects.get(id=dataset_id)
            except Dataset.DoesNotExist:
                return Response(
                    {"error": "Dataset not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Create PDF
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1e293b'),
                spaceAfter=30,
            )
            title = Paragraph("ChemEquip Visualizer - Equipment Report", title_style)
            elements.append(title)
            
            # Metadata
            meta_style = styles['Normal']
            elements.append(Paragraph(f"<b>Dataset:</b> {dataset.filename}", meta_style))
            elements.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
            elements.append(Paragraph(f"<b>Total Equipment:</b> {dataset.total_count}", meta_style))
            elements.append(Spacer(1, 0.3 * inch))
            
            # Summary Statistics
            elements.append(Paragraph("<b>Summary Statistics</b>", styles['Heading2']))
            summary_data = [
                ['Metric', 'Value'],
                ['Average Flowrate', f"{dataset.avg_flowrate:.2f} m³/h"],
                ['Average Pressure', f"{dataset.avg_pressure:.2f} bar"],
                ['Average Temperature', f"{dataset.avg_temperature:.2f} °C"],
            ]
            summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Equipment Data Table
            elements.append(Paragraph("<b>Equipment Details</b>", styles['Heading2']))
            table_data = [['Equipment', 'Type', 'Flow (m³/h)', 'Pressure (bar)', 'Temp (°C)']]
            for item in dataset.data[:20]:  # Limit to first 20 for PDF
                table_data.append([
                    item['equipment_name'],
                    item['type'],
                    f"{item['flowrate']:.2f}",
                    f"{item['pressure']:.2f}",
                    f"{item['temperature']:.2f}"
                ])
            
            data_table = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            data_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(data_table)
            
            # Build PDF
            doc.build(elements)
            buffer.seek(0)
            
            # Return PDF as download
            response = HttpResponse(buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
            return response
            
        except Exception as e:
            return Response(
                {"error": f"PDF generation failed: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
