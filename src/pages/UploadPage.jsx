import { Check, FileAudio, FileImage, FileVideo, LockKeyhole, UploadCloud } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analysisApi, mediaApi } from '../services/api'
import { useLanguage } from '../i18n'

export default function UploadPage() {
  const { t } = useLanguage()
  const [file, setFile] = useState(null)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const select = (next) => { if (!next) return; setError(''); setProgress(0); setFile(next) }
  const submit = async () => { if (!file) return; setProgress(1); try { const response = await mediaApi.upload(file, (event) => setProgress(Math.round((event.loaded / event.total) * 55))); const analysis = await analysisApi.create(response.data.id); setProgress(100); navigate(`/analysis/${analysis.data.id}`) } catch (requestError) { setError(requestError.message); setProgress(0) } }
  const fileType = file?.type?.startsWith('image') ? 'image' : file?.type?.startsWith('audio') ? 'audio' : 'video'
  const FileIcon = fileType === 'image' ? FileImage : fileType === 'audio' ? FileAudio : FileVideo
  const stages = ['uploading', 'preprocessing', 'features', 'analyzing', 'verification', 'reportReady']
  return <><header className="page-header"><div><p className="section-kicker">{t('dashboard.analyze')}</p><h1>{t('upload.title')}</h1><p className="page-copy">{t('upload.copy')}</p></div><span className="step-badge">WORKFLOW 01 / 03</span></header><div className="upload-layout"><section className="surface upload-surface"><div className="media-tabs"><button className="selected">{t('upload.allMedia')}</button><span>Image · Audio · Video</span></div><label className={`drop-zone ${file ? 'has-file' : ''}`} onDragOver={(event) => event.preventDefault()} onDrop={(event) => { event.preventDefault(); select(event.dataTransfer.files[0]) }}><input type="file" accept="audio/*,image/*,video/*" onChange={(event) => select(event.target.files[0])} /><UploadCloud className="upload-circle" /><strong>{file ? file.name : t('upload.drop')}</strong><small>{file ? `${(file.size / 1024 / 1024).toFixed(2)} MB · ${fileType} · ${t('upload.ready')}` : t('upload.browse')}</small></label>{error && <div className="form-error upload-error" role="alert">{error}</div>}{progress > 0 && <><div className="progress-track"><span style={{ width: `${progress}%` }} /></div><div className="analysis-stages">{stages.map((stage, index) => <span className={progress >= (index + 1) * 16 ? 'complete' : ''} key={stage}><i>{progress >= (index + 1) * 16 ? <Check size={10} /> : index + 1}</i>{t(`upload.${stage}`)}</span>)}</div></>}<div className="upload-actions"><span>PNG, JPG, WEBP, WAV, MP3, FLAC, MP4, MOV, WEBM</span><button className="primary-button" disabled={!file || progress > 0} onClick={submit}>{progress > 0 ? t('upload.progress') : t('upload.start')}</button></div></section><aside className="upload-aside"><div className="mini-note"><span>01</span><div><strong>{t('upload.secure')}</strong><p>{t('upload.secureCopy')}</p></div></div><div className="mini-note"><span>02</span><div><strong>{t('upload.signals')}</strong><p>{t('upload.signalsCopy')}</p></div></div><div className="mini-note"><span>03</span><div><strong>{t('upload.review')}</strong><p>{t('upload.reviewCopy')}</p></div></div><div className="privacy-note"><LockKeyhole size={18} /><span><strong>{t('upload.private')}</strong><br />{t('upload.privateCopy')}</span></div>{file && <div className="file-card"><FileIcon size={20} /><div><strong>{file.name}</strong><small>{t('upload.processing')}</small></div></div>}</aside></div></>
}
