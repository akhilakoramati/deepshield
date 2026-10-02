import { Check, ChevronDown, Globe2 } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { languages, useLanguage } from '../i18n'

export default function LanguageSelector({ compact = false }) {
  const { language, changeLanguage, t } = useLanguage()
  const [open, setOpen] = useState(false)
  const rootRef = useRef(null)
  const selected = languages.find(({ code }) => code === language) || languages[0]
  useEffect(() => {
    const closeOutside = (event) => { if (!rootRef.current?.contains(event.target)) setOpen(false) }
    const closeEscape = (event) => { if (event.key === 'Escape') setOpen(false) }
    document.addEventListener('mousedown', closeOutside)
    document.addEventListener('keydown', closeEscape)
    return () => { document.removeEventListener('mousedown', closeOutside); document.removeEventListener('keydown', closeEscape) }
  }, [])
  return <div className={`language-selector ${compact ? 'compact' : ''}`} ref={rootRef}>
    <button className="language-trigger" type="button" aria-haspopup="listbox" aria-expanded={open} onClick={() => setOpen((value) => !value)}>
      <Globe2 size={16} /><span>{compact ? selected.native : selected.code === 'en' ? 'English' : selected.native}</span><ChevronDown size={14} />
    </button>
    {open && <div className="language-dropdown" role="listbox" aria-label={t('settings.language')}>
      {languages.map(({ code, label, native }) => <button type="button" role="option" aria-selected={language === code} key={code} onClick={() => { changeLanguage(code); setOpen(false) }}>
        <span>{native}{code === 'en' ? ' · United States' : ''}</span>{language === code && <Check size={15} />}
        <span className="language-option-label">{label}</span>
      </button>)}
    </div>}
  </div>
}
