import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
    baseURL: '/api/v1', // Proxy will forward to http://127.0.0.1:8000/api/v1
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface UploadResponse {
    id: number;
    file: string;
    uploaded_at: string;
    message: string;
    count: number;
}

export interface Equipment {
    id: number;
    equipment_name: string;
    equipment_type: string;
    flowrate: number;
    pressure: number;
    temperature: number;
}

export interface SummaryStats {
    total_count: number;
    averages: {
        flowrate: number;
        pressure: number;
        temperature: number;
    };
    type_distribution: {
        equipment_type: string;
        count: number;
    }[];
}

export const uploadFile = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<UploadResponse>('/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const getEquipmentList = async (uploadId?: number) => {
    const params = uploadId ? { upload_id: uploadId } : {};
    const response = await api.get<Equipment[]>('/equipment/', { params });
    return response.data;
};

export const getSummaryStats = async (uploadId?: number) => {
    const params = uploadId ? { upload_id: uploadId } : {};
    const response = await api.get<SummaryStats>('/upload/summary/', { params });
    return response.data;
};

export default api;
