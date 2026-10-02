import { Search } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { analysisApi } from '../services/api'
import { useLanguage } from '../i18n'

const PAGE_SIZE = 6

export default function HistoryPage() {
  const { t } = useLanguage()
  const [history, setHistory] = useState({ items: [], page: 1, page_size: PAGE_SIZE, total: 0, total_pages: 1 })
  const [filters, setFilters] = useState({ search: '', media_type: '', verdict: '', risk_level: '', start_date: '', end_date: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const params = { page: history.page, page_size: PAGE_SIZE }
    Object.entries(filters).forEach(([key, value]) => { if (value) params[key] = value })
    analysisApi.history(params).then((response) => setHistory(response.data)).catch((requestError) => setError(requestError.message)).finally(() => setLoading(false))
  }, [filters, history.page])

  const updateFilter = (key, value) => { setLoading(true); setFilters((current) => ({ ...current, [key]: value })); setHistory((current) => ({ ...current, page: 1 })) }
  return <><header className="page-header"><div><p className="section-kicker">{t('navigation.history')} / 04</p><h1>{t('history.title')}</h1><p className="page-copy">{t('history.copy')}</p></div></header>{error && <div className="form-error" role="alert">{error}</div>}<section className="surface history-surface"><div className="history-toolbar"><label className="search-box"><Search size={18} /><input aria-label={t('history.search')} value={filters.search} onChange={(event) => updateFilter('search', event.target.value)} placeholder={t('history.search')} /></label><div className="history-filters"><select className="filter-button" value={filters.media_type} onChange={(event) => updateFilter('media_type', event.target.value)} aria-label={t('history.allMedia')}><option value="">{t('history.allMedia')}</option><option value="image">{t('dashboard.images')}</option><option value="audio">{t('dashboard.audio')}</option><option value="video">{t('dashboard.video')}</option></select><select className="filter-button" value={filters.verdict} onChange={(event) => updateFilter('verdict', event.target.value)} aria-label={t('history.allResults')}><option value="">{t('history.allResults')}</option><option value="REAL">{t('history.authentic')}</option><option value="FAKE">{t('history.manipulated')}</option></select><select className="filter-button" value={filters.risk_level} onChange={(event) => updateFilter('risk_level', event.target.value)} aria-label={t('history.allRisk')}><option value="">{t('history.allRisk')}</option><option value="low">{t('history.lowRisk')}</option><option value="moderate">{t('history.moderateRisk')}</option><option value="elevated">{t('history.elevatedRisk')}</option></select></div></div><div className="history-date-filters"><label>{t('history.from')}<input type="date" value={filters.start_date} onChange={(event) => updateFilter('start_date', event.target.value)} /></label><label>{t('history.to')}<input type="date" value={filters.end_date} onChange={(event) => updateFilter('end_date', event.target.value)} /></label></div>{loading ? <div className="empty-state">{t('history.loading')}</div> : history.items.length ? <div className="analysis-table"><div className="table-row table-head"><span>{t('history.analysis')}</span><span>{t('dashboard.type')}</span><span>{t('dashboard.result')}</span><span>{t('dashboard.date')}</span></div>{history.items.map((row) => <div className="table-row" key={row.id}><span className="file-name">#{row.id} · {row.media_name}</span><span>{row.media_type}</span><span><b className={`status-pill ${row.label === 'REAL' ? 'real-pill' : 'fake-pill'}`}>{row.label} · {row.confidence}%</b></span><span><Link to={`/analysis/${row.id}`}>{t('history.view')}</Link></span></div>)}</div> : <div className="empty-state"><div><strong>{t('history.empty')}</strong><p>{t('history.emptyCopy')}</p></div></div>}<div className="pagination"><span>{history.total} {t('history.resultCount')} · {t('history.page')} {history.page} / {history.total_pages}</span><div><button disabled={history.page <= 1 || loading} onClick={() => { setLoading(true); setHistory((current) => ({ ...current, page: current.page - 1 })) }}>{t('history.previous')}</button><button disabled={history.page >= history.total_pages || loading} onClick={() => { setLoading(true); setHistory((current) => ({ ...current, page: current.page + 1 })) }}>{t('history.next')}</button></div></div></section></>
}
