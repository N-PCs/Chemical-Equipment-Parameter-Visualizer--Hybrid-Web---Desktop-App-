from rest_framework import serializers
from core.models import Equipment, FileUpload

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'file', 'uploaded_at']
