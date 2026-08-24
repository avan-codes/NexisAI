import axios from 'axios';
import { storage } from '../utils/storage';

const client = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
});

client.interceptors.request.use((config) => {
  const token = storage.get('nexis_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      storage.remove('nexis_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  },
);

export default client;