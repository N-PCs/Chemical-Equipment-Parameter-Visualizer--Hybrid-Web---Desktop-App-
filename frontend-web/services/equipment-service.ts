
import { EquipmentData, EquipmentSummary, DatasetHistory } from '../types';
import { authService } from './auth-service';

const API_BASE = (import.meta as any).env?.VITE_API_BASE || 'http://localhost:8000/api';

export const equipmentService = {
  /**
   * Uploads file to backend for processing and storage.
   */
  async uploadFile(file: File): Promise<DatasetHistory> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE}/upload/`, {
      method: 'POST',
      headers: {
        ...authService.getAuthHeader(),
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Upload failed');
    }

    return await response.json();
  },

  /**
   * Triggers PDF generation on the backend and downloads the result.
   */
  async generatePdf(dataset: DatasetHistory): Promise<void> {
    const response = await fetch(`${API_BASE}/generate-pdf/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...authService.getAuthHeader(),
      },
      body: JSON.stringify({ id: dataset.id }),
    });

    if (!response.ok) {
      throw new Error('PDF generation failed');
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `equipment_report_${dataset.id}.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  },

  /**
   * Fetches dataset history from the backend.
   */
  async getHistory(): Promise<DatasetHistory[]> {
    const response = await fetch(`${API_BASE}/history/`, {
      headers: {
        ...authService.getAuthHeader(),
      },
    });

    if (!response.ok) return [];

    return await response.json();
  }
};
