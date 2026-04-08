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
  getCategorias: () => api.get('/categorias/'),
  createPartido: (data) => api.post('/partidos/', data),
  updatePartido: (id, data) => api.patch(`/partidos/${id}/`, data),
  deletePartido: (id) => api.delete(`/partidos/${id}/`),

  getDesignaciones: () => api.get('/designaciones/'),
  updateDesignacion: (id, status) => api.patch(`/designaciones/${id}/`, { status }),
  getArbitros: () => api.get('/arbitros/'),
  getUsers: () => api.get('/users/'),
  createUser: (data) => api.post('/users/', data),
  updateUser: (id, data) => api.patch(`/users/${id}/`, data),

  createDesignacion: (data) => api.post('/designaciones/', data),
  deleteDesignacion: (id) => api.delete(`/designaciones/${id}/`),

  getDisponibilidades: () => api.get('/disponibilidades/'),
  addDisponibilidad: (data) => api.post('/disponibilidades/', data),
  getMiPerfil: () => api.get('/mi-perfil/'),
  updateMiPerfil: (data) => api.patch('/mi-perfil/', data),
  downloadLiquidaciones: (params) => api.get('/liquidaciones/excel/', { params, responseType: 'blob' }),
  getVapidKey: () => api.get('/push/vapid-key/'),
  subscribePush: (subscription) => api.post('/push/subscribe/', subscription),
};

export default api;
