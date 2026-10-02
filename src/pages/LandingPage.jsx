import { AudioLines, CheckCircle2, FileImage, FileVideo, LockKeyhole, ScanSearch, ShieldCheck, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'

const features = [
  { icon: ScanSearch, title: 'Explainable detection', copy: 'Clear signals and confidence scores your team can act on, not just a binary verdict.' },
  { icon: LockKeyhole, title: 'Private by design', copy: 'Protected uploads, authenticated workspaces, and a deliberate approach to sensitive evidence.' },
  { icon: Sparkles, title: 'Media intelligence', copy: 'One workspace for image, audio, and video authenticity checks across your operation.' },
  { icon: CheckCircle2, title: 'Forensic-ready records', copy: 'Turn completed analyses into structured reports for review, escalation, or audit.' },
]

export default function LandingPage() {
  return <main className="landing">
    <nav className="landing-nav"><Link className="brand" to="/"><span className="brand-mark">DS</span>DeepShield</Link><div><a href="#platform">Platform</a><a href="#how-it-works">How it works</a><Link to="/login">Sign in</Link><Link className="primary-button" to="/register">Start analyzing <span>→</span></Link></div></nav>
    <section className="landing-hero"><div><p className="section-kicker">Media authenticity platform</p><h1>AI-powered <em>deepfake detection</em> for decisive teams.</h1><p>Understand whether media is authentic, manipulated, or inconclusive with a private analysis workspace built for investigations, trust & safety, and digital forensics.</p><div className="hero-actions"><Link className="primary-button" to="/register">Analyze media <span>→</span></Link><a className="outline-button" href="#platform">Explore DeepShield</a></div></div><div className="signal-card" aria-label="Interactive analysis preview"><h3>Live analysis signal</h3><div className="scan-ring"><span>78%</span></div><div className="scan-lines"><div><span>Face boundary</span><strong>consistent</strong></div><div><span>Compression map</span><strong>low variance</strong></div><div><span>Authenticity score</span><strong>high confidence</strong></div></div></div></section>
    <section className="landing-section" id="platform"><p className="section-kicker">Built for signal, not spectacle</p><h2>A clearer way to verify media.</h2><div className="feature-grid">{features.map(({ icon: Icon, title, copy }) => <article key={title}><Icon size={20} /><h3>{title}</h3><p>{copy}</p></article>)}</div></section>
    <section className="landing-section" id="how-it-works"><p className="section-kicker">Workflow</p><h2>From upload to evidence.</h2><div className="steps-grid">{[['01', 'Upload media', 'Bring in an image, audio clip, or video securely.'], ['02', 'AI analysis', 'Multiple forensic signals are evaluated together.'], ['03', 'Verify authenticity', 'Review the verdict, confidence, and risk context.'], ['04', 'Explainable results', 'Share a report that makes the reasoning legible.']].map(([number, title, copy]) => <article key={number}><span className="step-number">{number}</span><h3>{title}</h3><p>{copy}</p></article>)}</div></section>
    <section className="landing-section"><div className="privacy-band"><ShieldCheck size={24} /><div><h3>Designed for sensitive media</h3><p>Authenticated access, clear session status, and a workspace that keeps privacy visible throughout the analysis journey.</p></div></div></section>
    <footer className="landing-footer"><span>DeepShield · Media intelligence for teams that need to know.</span><span><FileImage size={13} /> Image <AudioLines size={13} /> Audio <FileVideo size={13} /> Video</span></footer>
  </main>
}
