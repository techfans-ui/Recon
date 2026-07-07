from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from meilisearch import Client
from typing import List

app = FastAPI(title="OpenData Ghost FR - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MEILI_URL = os.getenv("MEILI_URL", "http://meilisearch:7700")
MEILI_KEY = os.getenv("MEILI_KEY", "masterKey")

# Fallback sample data
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "data", "sample.json")
with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
    SAMPLE = json.load(f)

def get_meili_client():
    try:
        client = Client(MEILI_URL, MEILI_KEY)
        # lazy create index if not exists
        try:
            client.get_index("opendata")
        except Exception:
            client.create_index("opendata", {"primaryKey": "id"})
        return client
    except Exception:
        return None

client = get_meili_client()
index = client.index("opendata") if client else None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/index-sample")
def index_sample():
    """Index the bundled sample data into Meilisearch. Returns number of documents indexed."""
    if not client or not index:
        raise HTTPException(status_code=503, detail="Meilisearch client not available")
    docs = SAMPLE
    try:
        res = index.add_documents(docs)
        return {"updateId": res.get("updateId"), "count": len(docs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/search")
def search(q: str = Query(..., description="query string"), limit: int = 10):
    """Search endpoint: queries Meilisearch if available, otherwise local sample."""
    if index:
        try:
            res = index.search(q, {"limit": limit})
            return res
        except Exception as e:
            return {"error": str(e)}
    # fallback simple search
    hits = [item for item in SAMPLE if q.lower() in (item.get("title", "") + item.get("content", "")).lower()]
    return {"hits": hits[:limit], "nbHits": len(hits)}
