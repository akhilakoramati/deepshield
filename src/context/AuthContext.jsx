import { createContext, useState } from 'react'
import { authApi } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('deepshield_user') || 'null'))
  const [token, setToken] = useState(() => localStorage.getItem('deepshield_token'))

  const saveSession = (payload) => {
    localStorage.setItem('deepshield_token', payload.access_token)
    localStorage.setItem('deepshield_user', JSON.stringify(payload.user))
    setToken(payload.access_token)
    setUser(payload.user)
  }
  const login = async (payload) => saveSession((await authApi.login(payload)).data)
  const register = async (payload) => saveSession((await authApi.register(payload)).data)
  const logout = async () => { try { if (token) await authApi.logout() } catch {} finally { localStorage.removeItem('deepshield_token'); localStorage.removeItem('deepshield_user'); setToken(null); setUser(null) } }
  const value = { user, token, isAuthenticated: Boolean(token), login, register, logout }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export { AuthContext }
