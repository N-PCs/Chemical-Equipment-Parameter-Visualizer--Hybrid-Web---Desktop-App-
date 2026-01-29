from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import Equipment, FileUpload

class EquipmentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.csv_content = (
            b"Equipment Name, Type, Flowrate, Pressure, Temperature\n"
            b"Reactor A, Reactor, 100.0, 50.0, 80.0\n"
            b"Pump B, Pump, 50.0, 10.0, 25.0\n"
            b"Reactor C, Reactor, 110.0, 55.0, 85.0"
        )
        self.csv_file = SimpleUploadedFile("test_data.csv", self.csv_content, content_type="text/csv")

    def test_upload_csv(self):
        response = self.client.post('/api/v1/upload/', {'file': self.csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['count'], 3)
        self.assertEqual(Equipment.objects.count(), 3)
        self.assertEqual(FileUpload.objects.count(), 1)

    def test_summary_stats(self):
        # Upload first
        self.client.post('/api/v1/upload/', {'file': self.csv_file}, format='multipart')
        
        # Get summary
        response = self.client.get('/api/v1/upload/summary/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_count'], 3)
        
        # Avg flowrate: (100+50+110)/3 = 86.67
        self.assertAlmostEqual(response.data['averages']['flowrate'], 86.67, delta=0.01)

    def test_equipment_list(self):
         # Upload first
        upload_resp = self.client.post('/api/v1/upload/', {'file': self.csv_file}, format='multipart')
        upload_id = upload_resp.data['id']
        
        # List
        response = self.client.get(f'/api/v1/equipment/?upload_id={upload_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
