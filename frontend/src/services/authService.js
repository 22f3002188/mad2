// src/services/authService.js
import api from './api';

export async function loginUser(email, password) {
  const data = await api.post('/api/login', { email, password });
  localStorage.setItem('token', data.access_token); // Save token for future calls
  localStorage.setItem('user', JSON.stringify(data.user)); // Optional
  return data.user;
}

export async function registerUser(payload) {
  return await api.post('/api/signup', payload);
}
