const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }
  return res.json();
}

export const api = {
  listQuestions: (params = {}) => {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== '')
    ).toString();
    return request(`/api/questions${qs ? `?${qs}` : ''}`);
  },
  getQuestion: (id) => request(`/api/questions/${id}`),
  getTags: () => request('/api/questions/meta/tags'),
  toggleFavorite: (userId, questionId) =>
    request('/api/questions/favorites/toggle', {
      method: 'POST',
      body: JSON.stringify({ user_id: userId, question_id: questionId }),
    }),
  recentlyAttempted: (userId) => request(`/api/questions/recent?user_id=${userId}`),

  submitAttempt: (payload) =>
    request('/api/attempts/submit', { method: 'POST', body: JSON.stringify(payload) }),
  getHistory: (userId) => request(`/api/attempts/history?user_id=${userId}`),
  getStats: (userId) => request(`/api/attempts/stats?user_id=${userId}`),
};
