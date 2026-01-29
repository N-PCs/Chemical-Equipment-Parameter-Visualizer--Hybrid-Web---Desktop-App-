import requests
import os

class APIClient:
    def __init__(self, base_url="http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.token = None
        self.auth_url = "http://127.0.0.1:8000/api-token-auth/" # Independent of v1 prefix

    def login(self, username, password):
        try:
            response = requests.post(self.auth_url, json={'username': username, 'password': password})
            response.raise_for_status()
            data = response.json()
            self.token = data.get('token')
            return True
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return False

    def _get_headers(self):
        headers = {}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers

    def upload_csv(self, file_path):
        """
        Uploads a CSV file to the backend.
        """
        url = f"{self.base_url}/v1/upload/"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                # headers arg causes issues with multipart/form-data boundary if Content-Type is set manually.
                # Requests handles boundary automatically if separate files arg is passed.
                # But we need Auth header.
                response = requests.post(url, files=files, headers=self._get_headers())
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
        url = f"{self.base_url}/v1/upload/summary/"
        params = {}
        if upload_id:
            params['upload_id'] = upload_id
            
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
             print(f"Error fetching summary: {e}")
             return None

    def get_equipment_list(self, upload_id=None):
        """
        Fetches equipment list.
        """
        url = f"{self.base_url}/v1/equipment/"
        params = {}
        if upload_id:
            params['upload_id'] = upload_id
            
        try:
            response = requests.get(url, params=params, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
             print(f"Error fetching equipment: {e}")
             return None

    def download_report(self, upload_id, save_path):
        """
        Downloads the PDF report for a given upload_id.
        """
        url = f"{self.base_url}/v1/upload/{upload_id}/report/"
        try:
            response = requests.get(url, headers=self._get_headers(), stream=True)
            response.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error downloading report: {e}")
            return False
