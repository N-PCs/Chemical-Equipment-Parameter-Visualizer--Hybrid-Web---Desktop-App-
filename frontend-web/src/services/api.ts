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


export const setAuthToken = (token: string | null) => {
    if (token) {
        api.defaults.headers.common['Authorization'] = `Token ${token}`;
        localStorage.setItem('token', token);
    } else {
        delete api.defaults.headers.common['Authorization'];
        localStorage.removeItem('token');
    }
};

// Initialize token from storage
const storedToken = localStorage.getItem('token');
if (storedToken) {
    setAuthToken(storedToken);
}

export const login = async (username: string, password: string): Promise<string> => {
    // Note: The backend endpoint is at /api-token-auth/ (root level, not under /api/v1/)
    // Our proxy forwards /api -> http://127.0.0.1:8000/api
    // So we need to call /api-token-auth/ directly through the proxy or via absolute URL if proxy handles root.
    // However, vite proxy is: '/api': { target: 'http://127.0.0.1:8000' }
    // If we want to hit /api-token-auth/, we might need to adjust proxy or use full URL.
    // Let's assume we can add a proxy rule for /api-token-auth or just use the axios instance if we change baseURL.

    // Quick fix: create a temp axios call or adjust api instance. 
    // Since api instance has baseURL '/api/v1', we can use '.. /../api-token-auth/'? No that's messy.
    // Let's just use a fresh axios call for login to be safe, or adjust the path.

    // IF proxy is:
    // '/api': target:8000
    // Then /api/v1 -> 8000/api/v1.
    // We need 8000/api-token-auth/.
    // Let's try to fetch relative to root.

    const response = await axios.post('/api-token-auth/', { username, password }, {
        baseURL: '/', // Override base URL to use root relative path, assuming proxy handles /api-token-auth if configured.
        // WAIT. I didn't configure proxy for /api-token-auth. I only configured it for /api.
        // I should update vite.config.ts OR just change the backend URL in urls.py to be under /api/.
    });
    return response.data.token;
};

export default api;

