import { createContext, createElement, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import en from './locales/en.json'
import te from './locales/te.json'
import hi from './locales/hi.json'
import ta from './locales/ta.json'
import kn from './locales/kn.json'
import ml from './locales/ml.json'
import bn from './locales/bn.json'
import mr from './locales/mr.json'
import es from './locales/es.json'
import fr from './locales/fr.json'

const languageList = [
  { code: 'en', label: 'English (United States)' }, { code: 'te', label: 'Telugu' }, { code: 'hi', label: 'Hindi' },
  { code: 'ta', label: 'Tamil' }, { code: 'kn', label: 'Kannada' }, { code: 'ml', label: 'Malayalam' },
  { code: 'bn', label: 'Bengali' }, { code: 'mr', label: 'Marathi' }, { code: 'es', label: 'Spanish' }, { code: 'fr', label: 'French' },
]
export const languages = languageList.map(({ code, label }) => ({ code, label, native: new Intl.DisplayNames([code], { type: 'language' }).of(code) }))

const dictionaries = { en, te, hi, ta, kn, ml, bn, mr, es, fr }
const LanguageContext = createContext(null)
const getSavedLanguage = () => {
  const saved = localStorage.getItem('deepshield_language')
  return languages.some(({ code }) => code === saved) ? saved : 'en'
}
const lookup = (dictionary, key) => key.split('.').reduce((value, part) => value?.[part], dictionary)

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(getSavedLanguage)
  useEffect(() => { document.documentElement.lang = language }, [language])
  const changeLanguage = useCallback((code) => {
    if (!languages.some(({ code: supported }) => supported === code)) return
    localStorage.setItem('deepshield_language', code)
    setLanguage(code)
  }, [])
  const t = useCallback((key) => lookup(dictionaries[language], key) ?? lookup(en, key) ?? key, [language])
  const value = useMemo(() => ({ language, changeLanguage, t }), [language, changeLanguage, t])
  return createElement(LanguageContext.Provider, { value }, children)
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (!context) throw new Error('useLanguage must be used within LanguageProvider')
  return context
}
