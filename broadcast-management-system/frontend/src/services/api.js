import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authService = {
  signup: (username, email, password) =>
    api.post('/auth/signup', { username, email, password }),
  
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  
  getCurrentUser: () =>
    api.get('/auth/me'),
  
  logout: () =>
    api.post('/auth/logout'),
};

export const broadcastService = {
  listBroadcasts: (page = 1, perPage = 10, status = null) => {
    const params = { page, per_page: perPage };
    if (status) params.status = status;
    return api.get('/broadcasts', { params });
  },
  
  getBroadcast: (id) =>
    api.get(`/broadcasts/${id}`),
  
  createBroadcast: (title, message) =>
    api.post('/broadcasts', { title, message }),
  
  updateBroadcast: (id, data) =>
    api.put(`/broadcasts/${id}`, data),
  
  deleteBroadcast: (id) =>
    api.delete(`/broadcasts/${id}`),
  
  sendBroadcast: (id, targetUsers = []) =>
    api.post(`/broadcasts/${id}/send`, { target_users: targetUsers }),
  
  getUserNotifications: (page = 1, perPage = 10) =>
    api.get('/broadcasts/notifications/all', { params: { page, per_page: perPage } }),
};

export default api;
