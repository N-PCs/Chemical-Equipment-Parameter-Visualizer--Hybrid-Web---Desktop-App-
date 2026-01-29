import requests
import os

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api/v1"):
        self.base_url = base_url

    def upload_csv(self, file_path):
        """
        Uploads a CSV file to the backend.
        """
        url = f"{self.base_url}/upload/"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files)
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error uploading file: {e}")
            if hasattr(e.response, 'text'):
                 print(f"Response: {e.response.text}")
            return None

    def get_summary_stats(self, upload_id=None):
        """
        Fetches summary statistics.
        """
        url = f"{self.base_url}/upload/summary/"
        params = {}
        if upload_id:
            params['upload_id'] = upload_id
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
             print(f"Error fetching summary: {e}")
             return None

    def get_equipment_list(self, upload_id=None):
        """
        Fetches equipment list.
        """
        url = f"{self.base_url}/equipment/"
        params = {}
        if upload_id:
            params['upload_id'] = upload_id
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
             print(f"Error fetching equipment: {e}")
             return None
