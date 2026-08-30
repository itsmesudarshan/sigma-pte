const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export const authApi = {
  requestSignupOtp: (email, password) =>
    request('/api/auth/signup/request-otp', { method: 'POST', body: JSON.stringify({ email, password }) }),
  verifySignupOtp: (email, otp) =>
    request('/api/auth/signup/verify', { method: 'POST', body: JSON.stringify({ email, otp }) }),
  login: (email, password) =>
    request('/api/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  me: (token) =>
    request('/api/auth/me', { headers: { Authorization: `Bearer ${token}` } }),
};
