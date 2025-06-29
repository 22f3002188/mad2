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

export async function updateSubject(id, payload) {
  return await api.put(`/api/subjects/${id}`, payload, true);
}

export async function getChaptersBySubject(subjectId) {
  return await api.get(`/api/subjects/${subjectId}/chapters`, true);
}

export async function getAllUsers() {
  return await api.get('/api/admin/users', true); // authenticated
}

export async function deleteUserById(id) {
  return await api.delete(`/api/users/${id}`, true); // authenticated
}

export async function addChapter(subjectId, data) {
  return await api.post(`/api/subjects/${subjectId}/chapters`, data, true); // 'true' means it includes JWT
}

export async function updateChapter(chapterId, data) {
  return await api.put(`/api/chapters/${chapterId}`, data, true);
}


export async function deleteChapter(chapterId) {
  return await api.delete(`/api/chapters/${chapterId}`, true); // Authenticated DELETE
}

export async function getQuizzesByChapter(chapterId) {
  return await api.get(`/api/chapters/${chapterId}/quizzes`, true); // true => use JWT
}

export async function addQuiz(chapterId, data) {
  return await api.post(`/api/chapters/${chapterId}/quizzes`, data, true);
}

export async function updateQuiz(chapterId, quizId, data) {
  return await api.put(`/api/chapters/${chapterId}/quizzes/${quizId}`, data, true);
}


export async function deleteQuiz(chapterId, quizId) {
  return await api.delete(`/api/chapters/${chapterId}/quizzes/${quizId}`, true);
}

export async function getQuestionsByQuiz(quizId) {
  return await api.get(`/api/quizzes/${quizId}/questions`, true); // true = with auth
}

export async function deleteQuestion(quizId, questionId) {
  return await api.delete(`/api/quizzes/${quizId}/questions/${questionId}`, true);
}




