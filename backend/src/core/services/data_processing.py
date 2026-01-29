import pandas as pd
from django.db.models import Count, Avg
from core.models import Equipment, FileUpload

def process_csv(file_upload_instance):
    """
    Reads CSV from FileUpload instance, parses checks for required columns,
    and bulk creates Equipment records.
    """
    try:
        # Read CSV
        df = pd.read_csv(file_upload_instance.file.open())
        
        # Standardize columns (strip spaces, lowercase)
        df.columns = df.columns.str.strip().str.lower()
        
        # Mapping expected columns to model fields
        # Model: equipment_name, equipment_type, flowrate, pressure, temperature
        # CSV expected: Equipment Name, Type, Flowrate, Pressure, Temperature
        
        column_map = {
            'equipment name': 'equipment_name',
            'type': 'equipment_type',
            'flowrate': 'flowrate',
            'pressure': 'pressure',
            'temperature': 'temperature'
        }
        
        # validate columns
        missing_cols = [col for col in column_map.keys() if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns: {', '.join(missing_cols)}")
            
        # Rename columns to match model fields
        df = df.rename(columns=column_map)
        
        # Create Equipment objects
        equipment_list = []
        for _, row in df.iterrows():
            equipment_list.append(Equipment(
                file_upload=file_upload_instance,
                equipment_name=row['equipment_name'],
                equipment_type=row['equipment_type'],
                flowrate=row['flowrate'],
                pressure=row['pressure'],
                temperature=row['temperature']
            ))
            
        Equipment.objects.bulk_create(equipment_list)
        
        return len(equipment_list)
        
    except Exception as e:
        # If processing fails, delete the upload to avoid orphan records/bad state
        file_upload_instance.delete()
        raise e

def cleanup_old_uploads():
    """
    Keeps only the last 5 uploads. Deletes older ones.
    """
    uploads = FileUpload.objects.all()
    if uploads.count() > 5:
        # Keep top 5, delete rest. Ordering is -uploaded_at.
        to_delete = uploads[5:]
        for upload in to_delete:
            # File cleanup happens via signals usually, but explicit delete works for model
            upload.delete()

def get_summary_stats(file_upload_id=None):
    """
    Returns summary statistics.
    If file_upload_id provided, filters by that upload.
    Otherwise returns stats for the latest upload.
    """
    queryset = Equipment.objects.all()
    
    if file_upload_id:
        queryset = queryset.filter(file_upload_id=file_upload_id)
    else:
        # Get latest upload
        latest_upload = FileUpload.objects.first()
        if not latest_upload:
            return None
        queryset = queryset.filter(file_upload=latest_upload)
        
    total_count = queryset.count()
    if total_count == 0:
        return {}
        
    # Stats
    avg_flowrate = queryset.aggregate(Avg('flowrate'))['flowrate__avg']
    avg_pressure = queryset.aggregate(Avg('pressure'))['pressure__avg']
    avg_temperature = queryset.aggregate(Avg('temperature'))['temperature__avg']
    
    # Distribution
    type_distribution = list(queryset.values('equipment_type').annotate(count=Count('equipment_type')))
    
    return {
        'total_count': total_count,
        'averages': {
            'flowrate': round(avg_flowrate, 2),
            'pressure': round(avg_pressure, 2),
            'temperature': round(avg_temperature, 2)
        },
        'type_distribution': type_distribution
    }
