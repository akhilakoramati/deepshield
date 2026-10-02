import { useEffect, useState } from 'react'
import { Download, ShieldCheck } from 'lucide-react'
import { useParams } from 'react-router-dom'
import { reportApi } from '../services/api'
import { useLanguage } from '../i18n'

export default function ReportPage() {
  const { t } = useLanguage(); const { id } = useParams(); const [report, setReport] = useState(null); const [error, setError] = useState(''); const [busy, setBusy] = useState(false)
  useEffect(() => { reportApi.get(id).then((response) => setReport(response.data)).catch((requestError) => setError(requestError.message)) }, [id])
  const download = async () => { setBusy(true); try { const response = await reportApi.download(id); const url = URL.createObjectURL(response.data); const link = document.createElement('a'); link.href = url; link.download = `deepshield_report_${report.analysis.id}.pdf`; link.click(); URL.revokeObjectURL(url) } catch (requestError) { setError(requestError.message) } finally { setBusy(false) } }
  if (error) return <div className="form-error" role="alert">{error}</div>
  if (!report) return <div className="empty-state">{t('reports.loading')}</div>
  const result = report.analysis
  return <article className="report-document"><header><div><span className="brand-mark">DS</span><strong>DeepShield</strong></div><button className="primary-button" disabled={busy} onClick={download}><Download size={15} /> {busy ? t('reports.preparing') : t('reports.download')}</button></header><p className="section-kicker">{t('reports.forensic')}</p><h1>{report.title}</h1><p className="report-id">Report #{report.id} · Analysis #{result.id}</p><div className="report-grid"><div><span>{t('reports.status')}</span><strong>{result.status}</strong></div><div><span>{t('reports.prediction')}</span><strong>{result.label || 'Pending'}</strong></div><div><span>{t('reports.confidence')}</span><strong>{result.confidence != null ? `${result.confidence}%` : 'Pending'}</strong></div><div><span>{t('reports.format')}</span><strong>PDF</strong></div></div><section><h2>{t('reports.summary')}</h2><p>{result.details || t('reports.noSummary')}</p></section><section className="report-verification"><ShieldCheck size={20} /><div><strong>{t('reports.verification')}</strong><p>{t('reports.verificationCopy')}</p></div></section></article>
}
