import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || '/api' })

const getErrorMessage = (error) => {
  const detail = error.response?.data?.detail

  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0]
    if (typeof first === 'string') return first
    if (first?.msg) return first.msg
    if (first?.loc?.length) return `${first.loc[first.loc.length - 1]} is invalid.`
  }

  if (typeof detail === 'string') return detail
  if (typeof error.response?.data?.message === 'string') return error.response.data.message

  return 'The request could not be completed.'
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('deepshield_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use((response) => response, (error) => {
  if (error.response?.status === 401) {
    localStorage.removeItem('deepshield_token')
    localStorage.removeItem('deepshield_user')
  }
  if (!error.response) return Promise.reject(new Error('DeepShield API is offline. Start the backend on port 8000, then try again.'))
  return Promise.reject(new Error(getErrorMessage(error)))
})

export const authApi = {
  register: (payload) => api.post('/auth/register', payload),
  login: (payload) => api.post('/auth/login', payload),
  me: () => api.get('/auth/me'),
  changePassword: (payload) => api.post('/auth/change-password', payload),
  logout: () => api.post('/auth/logout'),
}

export const mediaApi = {
  upload: (file, onUploadProgress) => {
    const data = new FormData()
    data.append('file', file)
    return api.post('/media/upload', data, { onUploadProgress })
  },
  get: (id) => api.get(`/media/${id}`),
}

export const analysisApi = {
  create: (mediaId) => api.post('/analysis', { media_id: mediaId }),
  get: (id) => api.get(`/analysis/${id}`),
  history: (params = {}) => api.get('/analysis/history', { params }),
  remove: (id) => api.delete(`/analysis/${id}`),
}

export const dashboardApi = { stats: () => api.get('/dashboard/stats') }
export const reportApi = { list: () => api.get('/reports'), create: (analysisId, title) => api.post('/reports', { analysis_id: analysisId, title, format: 'pdf' }), get: (id) => api.get(`/reports/${id}`), download: (id) => api.get(`/reports/${id}/download`, { responseType: 'blob' }) }
export default api
