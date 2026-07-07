import { useState, useEffect, useRef } from 'react'
import Head from 'next/head'

const REGISTER = 'https://opendata.enokdev.com/register'
const LOGIN = 'https://opendata.enokdev.com/login'

// ============================================================
// Bilingual content catalog (English / Français)
// ============================================================
const T = {
  en: {
    htmlLang: 'en',
    metaDesc: 'Multi-source OSINT reconnaissance — automated, correlated, synthesized by AI.',
    navStatus: 'SYSTEM ONLINE | RECON ENGINE READY',
    login: 'LOGIN',
    startRecon: 'START_RECON →',
    heroEyebrow: 'SYSTEM ONLINE // RECON ENGINE READY',
    heroTitleA: 'Open-source intelligence,',
    heroTitleB: 'augmented.',
    heroLead: 'Multi-source OSINT reconnaissance — automated, correlated, synthesized by AI.',
    heroSub: 'No setup. No noise. Just intelligence.',
    statSources: 'Sources',
    statLatency: 'Latency',
    statAi: 'AI Model',
    scroll: 'SCROLL ▼',
    demoTag: 'LIVE DEMO',
    demoTitle: '$ Watch the engine run',
    demoTerminalTitle: 'opendata — recon terminal',
    scanning: 'SCANNING',
    done: 'DONE',
    capTag: 'CAPABILITIES',
    capTitle: 'Intelligence infrastructure',
    capabilities: [
      { tag: '[RECON_ENGINE]', title: 'Multi-Source Recon', body: 'Parallel interrogation across 10+ open data sources. GitHub, WHOIS, DNS, crt.sh, Shodan, HIBP, and more — simultaneously.', metric: '10+ sources' },
      { tag: '[CORRELATION]', title: 'Entity Correlation', body: 'Automatic cross-source entity matching with confidence scoring. Connects usernames, emails, IPs, and domains across datasets.', metric: '99.2% accuracy' },
      { tag: '[AI_SYNTHESIS]', title: 'Claude-Powered Intel', body: 'LLM-generated intelligence reports and interactive Q&A on your investigation data. Ask anything, get actionable answers.', metric: 'Claude Sonnet 4.6' },
    ],
    protoTag: 'PROTOCOL',
    protoTitle: 'How it works',
    steps: [
      { no: '01', key: 'INIT_TARGET', body: 'Enter email, username, domain, or IP address' },
      { no: '02', key: 'RECON_SCAN', body: 'Parallel interrogation of open data sources' },
      { no: '03', key: 'CORRELATE', body: 'Automatic cross-source entity correlation' },
      { no: '04', key: 'SYNTHESIZE', body: 'AI-generated intelligence report + Q&A' },
    ],
    pricingTag: 'PRICING',
    pricingTitle: 'Choose your plan',
    pricingNote: 'Pay with Wave, Orange Money, MTN Money or bank card.',
    plans: [
      { name: 'FREE', price: '0$', period: '/mo', featured: false, features: ['3 investigations/mo', '5 OSINT sources', '4 AI credits'], cta: 'START', href: REGISTER },
      { name: 'PRO', price: '5.99$', period: '/mo', featured: true, features: ['Unlimited investigations', '13 OSINT sources', 'Unlimited LLM', 'PDF export'], cta: 'TRY_PRO', href: 'https://opendata.enokdev.com/pricing' },
      { name: 'TEAM', price: '45.99$', period: '/mo', featured: false, features: ['Everything in Pro', 'Shared workspace', 'Invite teammates'], cta: 'TRY_TEAM', href: 'https://opendata.enokdev.com/pricing' },
      { name: 'ENTERPRISE', price: 'Custom', period: '', featured: false, features: ['Everything in Team', 'SSO / On-premise', 'Dedicated support', 'SLA'], cta: 'CONTACT_US', href: 'https://opendata.enokdev.com/pricing#enterprise' },
    ],
    pricingLink: '→ See the full comparison on /pricing',
    ctaReady: '▶ READY TO INITIALIZE',
    ctaTitleA: 'BEGIN YOUR',
    ctaTitleB: 'INVESTIGATION',
    ctaBody: 'Free during beta. No credit card. No limits. Start your first recon in under 60 seconds.',
    ctaBtn: 'INITIALIZE RECON →',
    ctaLoginHint: 'Already have an account?',
    ctaLoginLink: 'LOGIN →',
    footerTagline: '— OSINT v1.0 // Ghost Terminal',
    footerSys1: '[SYS] ALL RECON TARGETS ARE PUBLIC DATA ONLY',
    footerSys2: '2026 // OPERATIONAL',
    footerBuilt: 'BUILT BY',
  },
  fr: {
    htmlLang: 'fr',
    metaDesc: 'Reconnaissance OSINT multi-sources — automatisée, corrélée, synthétisée par IA.',
    navStatus: 'SYSTÈME EN LIGNE | MOTEUR DE RECON PRÊT',
    login: 'CONNEXION',
    startRecon: 'LANCER_RECON →',
    heroEyebrow: 'SYSTÈME EN LIGNE // MOTEUR DE RECON PRÊT',
    heroTitleA: 'Renseignement en source ouverte,',
    heroTitleB: 'augmenté.',
    heroLead: 'Reconnaissance OSINT multi-sources — automatisée, corrélée, synthétisée par IA.',
    heroSub: 'Sans configuration. Sans bruit. Juste du renseignement.',
    statSources: 'Sources',
    statLatency: 'Latence',
    statAi: 'Modèle IA',
    scroll: 'DÉFILER ▼',
    demoTag: 'DÉMO EN DIRECT',
    demoTitle: '$ Regardez le moteur tourner',
    demoTerminalTitle: 'opendata — terminal de recon',
    scanning: 'ANALYSE',
    done: 'TERMINÉ',
    capTag: 'CAPACITÉS',
    capTitle: 'Infrastructure de renseignement',
    capabilities: [
      { tag: '[MOTEUR_RECON]', title: 'Recon multi-sources', body: 'Interrogation parallèle de plus de 10 sources de données ouvertes. GitHub, WHOIS, DNS, crt.sh, Shodan, HIBP et plus — simultanément.', metric: '10+ sources' },
      { tag: '[CORRÉLATION]', title: "Corrélation d'entités", body: "Appariement automatique d'entités inter-sources avec score de confiance. Relie pseudos, e-mails, IP et domaines entre les jeux de données.", metric: '99,2 % de précision' },
      { tag: '[SYNTHÈSE_IA]', title: 'Renseignement par Claude', body: "Rapports de renseignement générés par LLM et Q&R interactif sur vos données d'enquête. Posez vos questions, obtenez des réponses concrètes.", metric: 'Claude Sonnet 4.6' },
    ],
    protoTag: 'PROTOCOLE',
    protoTitle: 'Comment ça marche',
    steps: [
      { no: '01', key: 'INIT_CIBLE', body: 'Saisir un e-mail, un pseudo, un domaine ou une adresse IP' },
      { no: '02', key: 'SCAN_RECON', body: 'Interrogation parallèle des sources de données ouvertes' },
      { no: '03', key: 'CORRÉLER', body: "Corrélation automatique d'entités inter-sources" },
      { no: '04', key: 'SYNTHÉTISER', body: 'Rapport de renseignement généré par IA + Q&R' },
    ],
    pricingTag: 'TARIFS',
    pricingTitle: 'Choisissez votre offre',
    pricingNote: 'Payez avec Wave, Orange Money, MTN Money ou carte bancaire.',
    plans: [
      { name: 'FREE', price: '0$', period: '/mois', featured: false, features: ['3 investigations/mois', '5 sources OSINT', '4 crédits IA'], cta: 'COMMENCER', href: REGISTER },
      { name: 'PRO', price: '5,99$', period: '/mois', featured: true, features: ['Investigations illimitées', '13 sources OSINT', 'LLM illimité', 'Export PDF'], cta: 'ESSAYER_PRO', href: 'https://opendata.enokdev.com/pricing' },
      { name: 'TEAM', price: '45,99$', period: '/mois', featured: false, features: ['Tout Pro inclus', 'Workspace partagé', 'Invitations collègues'], cta: 'ESSAYER_TEAM', href: 'https://opendata.enokdev.com/pricing' },
      { name: 'ENTERPRISE', price: 'Sur devis', period: '', featured: false, features: ['Tout Team inclus', 'SSO / On-premise', 'Support dédié', 'SLA'], cta: 'NOUS_CONTACTER', href: 'https://opendata.enokdev.com/pricing#enterprise' },
    ],
    pricingLink: '→ Voir la comparaison complète sur /pricing',
    ctaReady: '▶ PRÊT À INITIALISER',
    ctaTitleA: 'COMMENCEZ VOTRE',
    ctaTitleB: 'INVESTIGATION',
    ctaBody: 'Gratuit pendant la bêta. Sans carte bancaire. Sans limites. Lancez votre première recon en moins de 60 secondes.',
    ctaBtn: 'INITIALISER LA RECON →',
    ctaLoginHint: 'Vous avez déjà un compte ?',
    ctaLoginLink: 'CONNEXION →',
    footerTagline: '— OSINT v1.0 // Ghost Terminal',
    footerSys1: '[SYS] TOUTES LES CIBLES SONT DES DONNÉES PUBLIQUES UNIQUEMENT',
    footerSys2: '2026 // OPÉRATIONNEL',
    footerBuilt: 'CONÇU PAR',
  },
}

// Demo terminal lines per language (share the visual scan sequence).
const DEMO_LINES = {
  en: [
    { t: '$ opendata scan target@example.com', cls: 'prompt' },
    { t: '> INITIALIZING RECON ENGINE v1.0...', cls: 'muted' },
    { t: '> LOADING SOURCE CONNECTORS...', cls: 'muted' },
    { t: '> SYNCING PARALLEL DATA PORT ROUTERS...', cls: 'muted' },
    { t: '> SCANNING: github          [\u2713] match found', cls: 'ok' },
    { t: '> SCANNING: linkedin        [\u2713] profile indexed', cls: 'ok' },
    { t: '> SCANNING: twitter         [\u2713] 3 accounts', cls: 'ok' },
    { t: '> SCANNING: haveibeenpwned  [!] 2 breaches', cls: 'alert' },
    { t: '> SCANNING: shodan          [!] 1 exposed port', cls: 'alert' },
    { t: '> SCANNING: crt.sh          [\u2713] 8 certificates', cls: 'ok' },
    { t: '> SCANNING: whois           [\u2713] registrant matched', cls: 'ok' },
    { t: '', cls: 'muted' },
    { t: '[=== SCAN COMPLETE // 7 SOURCES // 9 ENTITIES MAPPED ===]', cls: 'accent' },
    { t: 'CONFIDENCE: HIGH // AI SYNTHESIS READY', cls: 'accent' },
  ],
  fr: [
    { t: '$ opendata scan cible@example.com', cls: 'prompt' },
    { t: '> INITIALISATION DU MOTEUR DE RECON v1.0...', cls: 'muted' },
    { t: '> CHARGEMENT DES CONNECTEURS DE SOURCES...', cls: 'muted' },
    { t: '> SYNCHRONISATION DES ROUTEURS PARALLÈLES...', cls: 'muted' },
    { t: '> ANALYSE : github          [\u2713] correspondance trouvée', cls: 'ok' },
    { t: '> ANALYSE : linkedin        [\u2713] profil indexé', cls: 'ok' },
    { t: '> ANALYSE : twitter         [\u2713] 3 comptes', cls: 'ok' },
    { t: '> ANALYSE : haveibeenpwned  [!] 2 fuites', cls: 'alert' },
    { t: '> ANALYSE : shodan          [!] 1 port exposé', cls: 'alert' },
    { t: '> ANALYSE : crt.sh          [\u2713] 8 certificats', cls: 'ok' },
    { t: '> ANALYSE : whois           [\u2713] titulaire trouvé', cls: 'ok' },
    { t: '', cls: 'muted' },
    { t: '[=== ANALYSE TERMINÉE // 7 SOURCES // 9 ENTITÉS CARTOGRAPHIÉES ===]', cls: 'accent' },
    { t: 'CONFIANCE : ÉLEVÉE // SYNTHÈSE IA PRÊTE', cls: 'accent' },
  ],
}

function LiveTerminal({ t, lang }) {
  const [visible, setVisible] = useState(0)
  const bodyRef = useRef(null)
  const lines = DEMO_LINES[lang]

  useEffect(() => {
    setVisible(0)
  }, [lang])

  useEffect(() => {
    const id = setInterval(() => {
      setVisible((v) => (v >= lines.length ? 0 : v + 1))
    }, 620)
    return () => clearInterval(id)
  }, [lines.length])

  useEffect(() => {
    if (bodyRef.current) bodyRef.current.scrollTop = bodyRef.current.scrollHeight
  }, [visible])

  return (
    <div className="terminal">
      <div className="terminal-bar">
        <span className="lights"><i className="l-red" /><i className="l-yellow" /><i className="l-green" /></span>
        <span className="title">{t.demoTerminalTitle}</span>
        <span className="badge">{visible >= lines.length ? t.done : t.scanning}</span>
      </div>
      <div className="terminal-body" ref={bodyRef}>
        {lines.slice(0, visible).map((l, i) => (
          <span key={i} className={`line ${l.cls}`}>{l.t || '\u00a0'}</span>
        ))}
        <span className="term-cursor" />
      </div>
    </div>
  )
}

function LangSwitch({ lang, setLang }) {
  return (
    <div className="lang-switch" role="group" aria-label="Language">
      <button className={lang === 'en' ? 'on' : ''} onClick={() => setLang('en')}>EN</button>
      <span className="sep">|</span>
      <button className={lang === 'fr' ? 'on' : ''} onClick={() => setLang('fr')}>FR</button>
    </div>
  )
}

export default function Home() {
  const [lang, setLang] = useState('en')
  const t = T[lang]

  // Persist + restore language choice on the client.
  useEffect(() => {
    const saved = typeof window !== 'undefined' && window.localStorage.getItem('opendata_lang')
    if (saved === 'en' || saved === 'fr') setLang(saved)
  }, [])
  useEffect(() => {
    if (typeof window !== 'undefined') {
      window.localStorage.setItem('opendata_lang', lang)
      document.documentElement.lang = t.htmlLang
    }
  }, [lang, t.htmlLang])

  return (
    <div className="wrap">
      <Head>
        <title>OPENDATA — OSINT v1.0 // Ghost Terminal</title>
        <meta name="description" content={t.metaDesc} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      {/* TOP BANNER */}
      <div className="app-banner">
        <h1 className="app-banner-title">Romaric Application</h1>
      </div>

      {/* NAV */}
      <nav className="nav">
        <div className="container nav-inner">
          <div className="brand">OPENDATA<span className="v"> // OSINT v1.0</span></div>
          <div className="nav-actions">
            <span className="status-pill"><span className="dot" /> {t.navStatus}</span>
            <LangSwitch lang={lang} setLang={setLang} />
            <a className="btn btn-ghost" href={LOGIN}>{t.login}</a>
            <a className="btn btn-primary" href={REGISTER}>{t.startRecon}</a>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <header className="hero">
        <div className="container">
          <div className="eyebrow">{t.heroEyebrow}</div>
          <h1>{t.heroTitleA}<br />{t.heroTitleB}<span className="blink">█</span></h1>
          <p className="lead">{t.heroLead}</p>
          <p className="sub">{t.heroSub}</p>
          <div className="hero-cta">
            <a className="btn btn-primary" href={REGISTER}>{t.startRecon}</a>
            <a className="btn btn-ghost" href={LOGIN}>{t.login}</a>
          </div>
          <div className="stats">
            <div className="stat"><div className="num">10+</div><div className="lbl">{t.statSources}</div></div>
            <div className="stat"><div className="num">&lt;3s</div><div className="lbl">{t.statLatency}</div></div>
            <div className="stat"><div className="num">CLAUDE</div><div className="lbl">{t.statAi}</div></div>
          </div>
          <div className="scroll-hint">{t.scroll}</div>
        </div>
      </header>

      {/* LIVE DEMO */}
      <section id="demo">
        <div className="container">
          <div className="section-tag">{t.demoTag}</div>
          <h2 className="section-title">{t.demoTitle}</h2>
          <LiveTerminal t={t} lang={lang} />
        </div>
      </section>

      {/* CAPABILITIES */}
      <section id="capabilities">
        <div className="container">
          <div className="section-tag">{t.capTag}</div>
          <h2 className="section-title">{t.capTitle}</h2>
          <div className="grid-3">
            {t.capabilities.map((c) => (
              <div className="card" key={c.tag}>
                <div className="tag">{c.tag}</div>
                <h3>{c.title}</h3>
                <p>{c.body}</p>
                <div className="metric">{c.metric}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section id="protocol">
        <div className="container">
          <div className="section-tag">{t.protoTag}</div>
          <h2 className="section-title">{t.protoTitle}</h2>
          <div className="steps">
            {t.steps.map((s) => (
              <div className="step" key={s.no}>
                <span className="idx">[{s.no}/04]</span>
                <div className="no">{s.no}</div>
                <h4>{s.key} →</h4>
                <p>{s.body}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* PRICING */}
      <section id="pricing">
        <div className="container">
          <div className="section-tag">{t.pricingTag}</div>
          <h2 className="section-title">{t.pricingTitle}</h2>
          <p className="pricing-note">{t.pricingNote}</p>
          <div className="grid-4">
            {t.plans.map((p) => (
              <div className={`plan ${p.featured ? 'featured' : ''}`} key={p.name}>
                <div className="name">[{p.name}]</div>
                <div className="price">{p.price}<small>{p.period}</small></div>
                <ul>{p.features.map((f) => <li key={f}>{f}</li>)}</ul>
                <a className={`btn ${p.featured ? 'btn-primary' : ''}`} href={p.href}>[{p.cta}]</a>
              </div>
            ))}
          </div>
          <div className="pricing-link">
            <a href="https://opendata.enokdev.com/pricing">{t.pricingLink}</a>
          </div>
        </div>
      </section>

      {/* FINAL CTA */}
      <section id="start">
        <div className="container">
          <div className="cta">
            <div className="ready">{t.ctaReady}</div>
            <h2>{t.ctaTitleA}<br />{t.ctaTitleB}</h2>
            <p>{t.ctaBody}</p>
            <a className="btn btn-primary" href={REGISTER}>{t.ctaBtn}</a>
            <div className="login-hint">{t.ctaLoginHint} <a href={LOGIN}>{t.ctaLoginLink}</a></div>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <div className="container footer-grid">
          <div>
            <div className="brand">OPENDATA<span className="v"> {t.footerTagline}</span></div>
            <div className="sys">{t.footerSys1}</div>
            <div className="sys">{t.footerSys2}</div>
          </div>
          <div className="links" style={{ textAlign: 'right' }}>
            <div>{t.footerBuilt} <a className="accent" href="https://enokdev-com.vercel.app/">ENOKDEV</a></div>
            <div style={{ marginTop: 8 }}>
              APPS:
              <a href="https://notepilote.enokdev.com/">NotePilote</a> |
              <a href="https://idea2mvp.enokdev.com/">Idea2MVP</a>
            </div>
            <div style={{ marginTop: 8 }}>
              <a href="https://www.linkedin.com/in/enokdev/">LinkedIn</a>
              <a href="https://github.com/tky0065">GitHub</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

