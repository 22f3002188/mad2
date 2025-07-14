const API_BASE_URL = 'http://127.0.0.1:5000';

function getToken() {
  return localStorage.getItem('token');
}

function getAuthHeaders() {
  const token = getToken();
  return token
    ? {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`, 
      }
    : {
        'Content-Type': 'application/json',
      };
}

async function post(endpoint, body, auth = false) {
  const headers = auth ? getAuthHeaders() : { 'Content-Type': 'application/json' };
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'POST',
    headers,
    body: JSON.stringify(body),
  });
  return handleResponse(response);
}

async function get(endpoint, auth = false) {
  const headers = auth ? getAuthHeaders() : { 'Content-Type': 'application/json' };
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'GET',
    headers,
  });
  return handleResponse(response);
}

async function put(endpoint, body, auth = false) {
  const headers = auth ? getAuthHeaders() : { 'Content-Type': 'application/json' };
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(body),
  });
  return handleResponse(response);
}

async function del(endpoint, auth = false) {
  const headers = auth ? getAuthHeaders() : { 'Content-Type': 'application/json' };
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: 'DELETE',
    headers,
  });
  return handleResponse(response);
}

async function handleResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.error || 'API request failed');
  }
  return data;
}

export default {
  get,
  post,
  put,
  delete: del, 
  getToken,
};
