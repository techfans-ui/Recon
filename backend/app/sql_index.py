import os
import sqlite3
import json
from typing import List, Dict, Any

BASE = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE, "opendata.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(docs: List[Dict[str, Any]] = None):
    conn = get_conn()
    cur = conn.cursor()
    # Try to create an FTS5 virtual table; if not available, fall back to a normal table
    try:
        cur.execute("CREATE VIRTUAL TABLE IF NOT EXISTS opendata_fts USING fts5(id, title, content, source, date, tokenize='unicode61')")
        conn.commit()
        use_fts = True
    except Exception:
        # Fallback: regular table
        cur.execute("CREATE TABLE IF NOT EXISTS opendata (id TEXT PRIMARY KEY, title TEXT, content TEXT, source TEXT, date TEXT)")
        conn.commit()
        use_fts = False

    if docs:
        index_docs(docs, conn=conn, use_fts=use_fts)

    return conn, use_fts

def index_docs(docs: List[Dict[str, Any]], conn: sqlite3.Connection = None, use_fts: bool = None):
    close = False
    if conn is None:
        conn, use_fts = init_db()
        close = True
    cur = conn.cursor()
    if use_fts:
        # REPLACE via insert into FTS table
        for d in docs:
            cur.execute("INSERT INTO opendata_fts (id, title, content, source, date) VALUES (?, ?, ?, ?, ?)",
                        (str(d.get("id")), d.get("title"), d.get("content"), d.get("source"), d.get("date")))
    else:
        for d in docs:
            cur.execute("INSERT OR REPLACE INTO opendata (id, title, content, source, date) VALUES (?, ?, ?, ?, ?)",
                        (str(d.get("id")), d.get("title"), d.get("content"), d.get("source"), d.get("date")))
    conn.commit()
    if close:
        conn.close()

def search(q: str, limit: int = 10):
    conn, use_fts = init_db()
    cur = conn.cursor()
    results = []
    if use_fts:
        try:
            # Use FTS5 MATCH query; sanitize single quotes
            query = q.replace("'", "''")
            stmt = "SELECT id, title, content, source, date FROM opendata_fts WHERE opendata_fts MATCH ? LIMIT ?"
            cur.execute(stmt, (query, limit))
            rows = cur.fetchall()
            for r in rows:
                results.append({k: r[k] for k in r.keys()})
        except Exception:
            pass
    else:
        # Fallback to simple LIKE search across title/content
        pattern = f"%{q}%"
        stmt = "SELECT id, title, content, source, date FROM opendata WHERE title LIKE ? OR content LIKE ? LIMIT ?"
        cur.execute(stmt, (pattern, pattern, limit))
        rows = cur.fetchall()
        for r in rows:
            results.append({k: r[k] for k in r.keys()})

    conn.close()
    return results
