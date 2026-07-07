import { useState, useRef } from 'react'
import axios from 'axios'

function highlight(text, q){
  if(!q) return text
  try{
    const re = new RegExp(`(${q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")})`, 'ig')
    return text.replace(re, '<mark>$1</mark>')
  }catch(e){
    return text
  }
}

export default function Home(){
  const [q, setQ] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])
  const inputRef = useRef()

  async function doSearch(e){
    e && e.preventDefault()
    if(!q) return
    setLoading(true)
    setHistory(h=>[q,...h].slice(0,10))
    try{
      const res = await axios.get(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/search`, { params: { q } })
      setResults(res.data)
    }catch(err){
      setResults({error: err.message})
    }finally{setLoading(false); inputRef.current && inputRef.current.focus()}
  }

  return (
    <div style={{background:'#000', color:'#0f0', minHeight:'100vh', padding:20, fontFamily:'monospace'}}>
      <h1>OpenData Ghost — Terminal OSINT (FR)</h1>
      <div className="terminal">
        <form onSubmit={doSearch} style={{display:'flex', gap:8, alignItems:'center'}}>
          <label>Requête:</label>
          <input ref={inputRef} value={q} onChange={e=>setQ(e.target.value)} style={{flex:1, background:'#000', color:'#0f0', border:'1px solid #0f0', padding:8}} />
          <button type="submit">Chercher</button>
          <span className="cursor" aria-hidden></span>
        </form>

        {history.length>0 && (
          <div style={{marginTop:12}}>
            <strong>Historique:</strong>
            <div>{history.join(' — ')}</div>
          </div>
        )}

        {loading && <p>Recherche en cours...</p>}
        {results && (
          <div style={{marginTop:20}}>
            {results.error && <div style={{color:'red'}}>Erreur: {results.error}</div>}
            {results.hits && results.hits.length>0 && (
              <ul>
                {results.hits.map(hit=> (
                  <li key={hit.id} style={{marginBottom:12}}>
                    <div className="hit-title">{hit.title}</div>
                    <div className="hit-source">{hit.source} • {hit.date}</div>
                    <div className="hit-content" dangerouslySetInnerHTML={{__html: highlight(hit.content || '', q)}} />
                  </li>
                ))}
              </ul>
            )}
            {!results.hits && <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(results, null, 2)}</pre>}
          </div>
        )}
      </div>
    </div>
  )
}
