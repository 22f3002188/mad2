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

export async function logoutUser() {
  await api.post('/api/logout', {}, true); // requires JWT token
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

export async function addSubject(subject) {
  return await api.post('/api/subjects', subject, true); // true = authenticated
}

export async function getSubjects() {
  return await api.get('/api/get_subjects', true); // ✅ Authenticated GET
}

export async function deleteSubject(id) {
  return await api.delete(`/api/subjects/${id}`, true);
}