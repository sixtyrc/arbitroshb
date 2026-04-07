import axios from 'axios';

const API_URL = '/api'; // Gracias al proxy en vite.config.js al usar npm run dev

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor para inyectar el token JWT en cada petición
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  login: async (username, password) => {
    const response = await api.post('/token/', { username, password });
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
    }
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};

export const gestionService = {
  getPartidos: () => api.get('/partidos/'),
  getDesignaciones: () => api.get('/designaciones/'),
  updateDesignacion: (id, status) => api.patch(`/designaciones/${id}/`, { status }),
  getDisponibilidades: () => api.get('/disponibilidades/'),
  addDisponibilidad: (data) => api.post('/disponibilidades/', data),
};

export default api;
