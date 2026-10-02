import { ChevronDown, FileText, History, LayoutDashboard, LogOut, Settings, ShieldCheck, UserRound, Upload } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { useLanguage } from '../i18n'
import LanguageSelector from '../components/LanguageSelector'

const links = [{ to: '/dashboard', label: 'overview', icon: LayoutDashboard }, { to: '/upload', label: 'newAnalysis', icon: Upload }, { to: '/history', label: 'history', icon: History }, { to: '/reports', label: 'reports', icon: FileText }, { to: '/settings', label: 'settings', icon: Settings }]

export default function DashboardLayout() {
  const { user, logout } = useAuth()
  const { t } = useLanguage()
  const [profileOpen, setProfileOpen] = useState(false)
  const profileMenuRef = useRef(null)
  useEffect(() => {
    const closeOnOutsideClick = (event) => { if (!profileMenuRef.current?.contains(event.target)) setProfileOpen(false) }
    const closeOnEscape = (event) => { if (event.key === 'Escape') setProfileOpen(false) }
    document.addEventListener('mousedown', closeOnOutsideClick)
    document.addEventListener('keydown', closeOnEscape)
    return () => { document.removeEventListener('mousedown', closeOnOutsideClick); document.removeEventListener('keydown', closeOnEscape) }
  }, [])
  return <div className="product-shell"><header className="product-topbar"><NavLink className="brand" to="/dashboard"><span className="brand-mark">DS</span><span>DeepShield</span></NavLink><div className="top-status"><span className="status-dot" />{t('shell.detection')} <i /> {t('shell.secure')}</div><div className="header-actions"><LanguageSelector compact /><div className="profile-menu" ref={profileMenuRef}><button className={`profile ${profileOpen ? 'open' : ''}`} aria-expanded={profileOpen} aria-haspopup="menu" onClick={() => setProfileOpen(!profileOpen)}><span className="avatar">{user?.full_name?.slice(0, 2).toUpperCase() || 'DS'}</span><span>{user?.full_name || 'Analyst'}</span><ChevronDown className="profile-chevron" size={16} /></button>{profileOpen && <div className="profile-dropdown" role="menu"><NavLink to="/settings" role="menuitem" onClick={() => setProfileOpen(false)}><UserRound size={17} /><span>{t('navigation.profile')}</span></NavLink><NavLink to="/settings" role="menuitem" onClick={() => setProfileOpen(false)}><Settings size={17} /><span>{t('navigation.settings')}</span></NavLink><div className="profile-menu-divider" /><button role="menuitem" onClick={async () => { setProfileOpen(false); await logout() }}><LogOut size={17} /><span>{t('navigation.logout')}</span></button></div>}</div></div></header><div className="product-body"><nav className="sidebar"><div className="side-label">{t('navigation.workspace')}</div>{links.map(({ to, label, icon: Icon }) => <NavLink key={to} className={({ isActive }) => isActive ? 'active' : ''} to={to}><Icon size={16} /><span>{t(`navigation.${label}`)}</span></NavLink>)}<div className="side-divider" /><div className="side-label">{t('navigation.account')}</div><button onClick={logout}><LogOut size={16} /><span>{t('navigation.logout')}</span></button><div className="sidebar-footer"><div className="side-help"><ShieldCheck size={18} /><span><strong>{t('navigation.protected')}</strong><br />{t('navigation.privacy')}</span></div></div></nav><main className="content"><Outlet /></main></div></div>
}
