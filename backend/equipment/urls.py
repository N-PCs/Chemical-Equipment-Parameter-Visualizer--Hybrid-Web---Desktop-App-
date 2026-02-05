"""
Equipment App - URL Configuration
"""
from django.urls import path
from .views import EquipmentUploadView, DatasetHistoryView, GeneratePDFView, api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('upload/', EquipmentUploadView.as_view(), name='equipment-upload'),
    path('history/', DatasetHistoryView.as_view(), name='dataset-history'),
    path('generate-pdf/', GeneratePDFView.as_view(), name='generate-pdf'),
]
