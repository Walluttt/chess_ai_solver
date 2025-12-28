import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const auth = {
  register: (data: { email: string; username: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  login: (username: string, password: string) =>
    api.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  me: () => api.get('/auth/me'),
}

// Games
export const games = {
  create: (data: {
    mode: string
    ai_difficulty?: number
    time_control?: string
    is_ranked?: boolean
  }) => api.post('/games/create', data),
  get: (gameId: number) => api.get(`/games/${gameId}`),
  move: (gameId: number, move: {
    from_row: number
    from_col: number
    to_row: number
    to_col: number
    promotion?: string
  }) => api.post(`/games/${gameId}/move`, move),
  history: () => api.get('/games/user/history'),
}

// Users
export const users = {
  getProfile: () => api.get('/users/me'),
  getUser: (userId: number) => api.get(`/users/${userId}`),
  update: (data: { full_name?: string; avatar_url?: string }) =>
    api.put('/users/me', data),
}

// Rankings
export const rankings = {
  leaderboard: (timeControl: string = 'rapid', limit: number = 100) =>
    api.get(`/rankings/leaderboard?time_control=${timeControl}&limit=${limit}`),
  getUserRanking: (userId: number) => api.get(`/rankings/user/${userId}`),
}

export default api
