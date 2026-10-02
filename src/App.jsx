import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { useEffect } from 'react'
import './App.css'
import { AuthProvider } from './context/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import DashboardLayout from './layouts/DashboardLayout'
import AnalysisResultPage from './pages/AnalysisResultPage'
import AuthPage from './pages/AuthPage'
import DashboardPage from './pages/DashboardPage'
import HistoryPage from './pages/HistoryPage'
import LandingPage from './pages/LandingPage'
import ReportPage from './pages/ReportPage'
import ReportsPage from './pages/ReportsPage'
import SettingsPage from './pages/SettingsPage'
import UploadPage from './pages/UploadPage'
import { LanguageProvider } from './i18n'

export default function App() {
  useEffect(() => {
    document.documentElement.dataset.theme = localStorage.getItem('deepshield_theme') || 'dark'
  }, [])
  return <LanguageProvider><BrowserRouter><AuthProvider><Routes><Route path="/" element={<LandingPage />} /><Route path="/login" element={<AuthPage mode="login" />} /><Route path="/register" element={<AuthPage mode="register" />} /><Route element={<ProtectedRoute />}><Route element={<DashboardLayout />}><Route path="/dashboard" element={<DashboardPage />} /><Route path="/upload" element={<UploadPage />} /><Route path="/analysis/:id" element={<AnalysisResultPage />} /><Route path="/history" element={<HistoryPage />} /><Route path="/reports" element={<ReportsPage />} /><Route path="/reports/:id" element={<ReportPage />} /><Route path="/settings" element={<SettingsPage />} /></Route></Route><Route path="*" element={<Navigate to="/" replace />} /></Routes></AuthProvider></BrowserRouter></LanguageProvider>
}
