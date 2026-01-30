"""
Equipment App - URL Configuration
"""
from django.urls import path
from .views import EquipmentUploadView, DatasetHistoryView, GeneratePDFView

urlpatterns = [
    path('upload/', EquipmentUploadView.as_view(), name='equipment-upload'),
    path('history/', DatasetHistoryView.as_view(), name='dataset-history'),
    path('generate-pdf/', GeneratePDFView.as_view(), name='generate-pdf'),
]
