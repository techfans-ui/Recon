import { useState, useRef } from 'react'
import Head from 'next/head'
import axios from 'axios'

function highlight(text, q) {
  if (!q) return text
  try {
    const re = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'ig')
    return text.replace(re, '<mark>$1</mark>')
  } catch (e) {
    return text
  }
}

export default function Search() {
  const [q, setQ] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const inputRef = useRef()

  async function doSearch(e) {
    e && e.preventDefault()
    if (!q) return
    setLoading(true)
    setHistory((h) => [q, ...h].slice(0, 10))
    try {
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/search`,
        { params: { q } }
      )
      setResults(res.data)
    } catch (err) {
      setResults({ error: err.message })
    } finally {
      setLoading(false)
      inputRef.current && inputRef.current.focus()
    }
  }

  return (
    <div className="wrap container" style={{ paddingTop: 40, paddingBottom: 40 }}>
      <Head>
        <title>OPENDATA — Recon Terminal</title>
      </Head>
      <h1 className="accent">OPENDATA — Terminal OSINT</h1>
      <div className="terminal" style={{ maxWidth: 900 }}>
        <div className="terminal-body">
          <form onSubmit={doSearch} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <label>Requête:</label>
            <input
              ref={inputRef}
              value={q}
              onChange={(e) => setQ(e.target.value)}
              style={{ flex: 1, background: '#05070a', color: 'var(--accent)', border: '1px solid var(--border)', padding: 8, fontFamily: 'inherit' }}
            />
            <button className="btn" type="submit">Chercher</button>
          </form>

          {history.length > 0 && (
            <div style={{ marginTop: 12 }}>
              <strong className="muted">Historique:</strong>
              <div className="muted">{history.join(' — ')}</div>
            </div>
          )}

          {loading && <p className="muted">Recherche en cours...</p>}
          {results && (
            <div style={{ marginTop: 20 }}>
              {results.error && <div className="alert">Erreur: {results.error}</div>}
              {results.hits && results.hits.length > 0 && (
                <ul style={{ listStyle: 'none', padding: 0 }}>
                  {results.hits.map((hit) => (
                    <li key={hit.id} style={{ marginBottom: 16 }}>
                      <div className="accent">{hit.title}</div>
                      <div className="muted">{hit.source} • {hit.date}</div>
                      <div dangerouslySetInnerHTML={{ __html: highlight(hit.content || '', q) }} />
                    </li>
                  ))}
                </ul>
              )}
              {!results.hits && <pre style={{ whiteSpace: 'pre-wrap' }}>{JSON.stringify(results, null, 2)}</pre>}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
