import api from './api';

export async function loginUser(email, password) {
  const data = await api.post('/api/login', { email, password });
  localStorage.setItem('token', data.access_token); 
  localStorage.setItem('user', JSON.stringify(data.user)); 
  return data.user;
}

export async function registerUser(payload) {
  return await api.post('/api/signup', payload);
}


export async function logoutUser() {
  await api.post('/api/logout', {}, true); 
  localStorage.removeItem('token');
  localStorage.removeItem('user');
}

export async function addSubject(subject) {
  return await api.post('/api/subjects', subject, true); 
}

export async function getSubjects() {
  return await api.get('/api/get_subjects', true); 
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
  return await api.get('/api/admin/users', true); 
}

export async function deleteUserById(id) {
  return await api.delete(`/api/users/${id}`, true); 
}

export async function addChapter(subjectId, data) {
  return await api.post(`/api/subjects/${subjectId}/chapters`, data, true); 
}

export async function updateChapter(chapterId, data) {
  return await api.put(`/api/chapters/${chapterId}`, data, true);
}


export async function deleteChapter(chapterId) {
  return await api.delete(`/api/chapters/${chapterId}`, true); 
}

export async function getQuizzesByChapter(chapterId) {
  return await api.get(`/api/chapters/${chapterId}/quizzes`, true); 
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
  return await api.get(`/api/quizzes/${quizId}/questions`, true); 
}

export async function deleteQuestion(quizId, questionId) {
  return await api.delete(`/api/quizzes/${quizId}/questions/${questionId}`, true);
}

export async function addQuestionToQuiz(quizId, data) {
  return await api.post(`/api/quizzes/${quizId}/questions`, data, true);
}

export async function updateQuestion(quizId, questionId, data) {
  return await api.put(`/api/quizzes/${quizId}/questions/${questionId}`, data, true);
}

export async function getUserScores() {
  return await api.get('/api/user/scores', true); 
}

export async function getAdminSummary() {
  return await api.get('/api/admin/summary', true); 
}

export async function getUserSummary() {
  return await api.get('/api/quizzes_charts', true); 
}

export async function searchAPI(query) {
  return await api.get(`/api/search?query=${encodeURIComponent(query)}`, true); 
}

export async function exportUserCSV() {
  return await api.post('/api/export_csv', {}, true); 
}


