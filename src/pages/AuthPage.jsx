import { Eye, EyeOff, ShieldCheck } from 'lucide-react'
import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import AuthVisual from '../components/AuthVisual'
import { useAuth } from '../hooks/useAuth'

export default function AuthPage({ mode }) {
  const register = mode === 'register'
  const { login, register: createAccount } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [password, setPassword] = useState('')
  const strength = password.length >= 12 ? 'Strong password' : password.length >= 8 ? 'Good password' : 'Use 8+ characters'
  const submit = async (event) => {
    event.preventDefault()
    setError('')
    const form = new FormData(event.currentTarget)
    const email = String(form.get('email') || '').trim()
    const passwordValue = String(form.get('password') || '')

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError('Please enter a valid email address.')
      return
    }

    const payload = { email, password: passwordValue }
    if (register) payload.full_name = form.get('full_name')
    if (register && passwordValue !== String(form.get('confirm_password') || '')) { setError('Passwords do not match.'); return }
    setBusy(true)
    try { await (register ? createAccount(payload) : login(payload)); navigate(location.state?.from?.pathname || '/dashboard', { replace: true }) } catch (requestError) { setError(requestError.message) } finally { setBusy(false) }
  }
  return <main className="auth-layout"><aside className="auth-aside"><Link className="brand light" to="/"><span className="brand-mark">DS</span>DeepShield</Link><div className="auth-quote"><p className="eyebrow">Secure media intelligence</p><h1>Trust the signal.</h1><p>Understand what your media is telling you with an analysis workspace built to keep sensitive evidence in focus.</p></div><AuthVisual /><span className="aside-foot">Encrypted workspace · Evidence stays yours</span></aside><section className="auth-card"><div className="auth-form"><Link className="mobile-brand brand" to="/"><span className="brand-mark">DS</span>DeepShield</Link><p className="section-kicker">{register ? 'Create your workspace' : 'Welcome back'}</p><h2>{register ? 'Start with clarity.' : 'Sign in to DeepShield.'}</h2><p className="form-copy">{register ? 'Bring your media verification workflow into one protected workspace.' : 'Continue to your media authenticity workspace.'}</p>{error && <div className="form-error" role="alert">{error}</div>}<form onSubmit={submit}>{register && <label>Full name<input name="full_name" required minLength="2" autoComplete="name" placeholder="Alex Morgan" /></label>}<label>Email<input name="email" required type="email" autoComplete="email" placeholder="you@company.com" /></label><label>Password<div className="password-field"><input name="password" required minLength="8" type={showPassword ? 'text' : 'password'} autoComplete={register ? 'new-password' : 'current-password'} value={password} onChange={(event) => setPassword(event.target.value)} placeholder="Enter your password" /><button type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword(!showPassword)}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div>{register && <small className="password-hint">{strength}</small>}</label>{register && <label>Confirm password<input name="confirm_password" required minLength="8" type="password" autoComplete="new-password" placeholder="Repeat your password" /></label>}{!register && <div className="auth-options"><label className="check-label"><input type="checkbox" name="remember" /> Remember me</label><button type="button" className="text-button">Forgot password?</button></div>}<button className="primary-button full" disabled={busy}>{busy ? 'Authenticating…' : register ? 'Create secure workspace' : 'Continue to workspace'} <span>→</span></button></form><div className="auth-assurance"><ShieldCheck size={15} /><span><strong>Private by default.</strong> Your uploads are only visible to your authenticated workspace.</span></div><p className="switch-copy">{register ? 'Already registered?' : 'New to DeepShield?'} <Link to={register ? '/login' : '/register'}>{register ? 'Sign in' : 'Create an account'}</Link></p></div></section></main>
}
