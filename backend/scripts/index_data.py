"""Index sample data into Meilisearch (run inside backend container).
Usage: python scripts/index_data.py
"""
import os
import json
import time
from meilisearch import Client
from app import sql_index

MEILI_URL = os.getenv("MEILI_URL", "http://meilisearch:7700")
MEILI_KEY = os.getenv("MEILI_KEY", "masterKey")

BASE = os.path.dirname(os.path.dirname(__file__))
SAMPLE_PATH = os.path.join(BASE, "app", "data", "sample.json")

with open(SAMPLE_PATH, "r", encoding="utf-8") as f:
    docs = json.load(f)

def wait_for_meili(url, timeout=30):
    from urllib.parse import urlparse
    import requests
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False

if wait_for_meili(MEILI_URL, timeout=10):
    client = Client(MEILI_URL, MEILI_KEY)
    try:
        client.get_index("opendata")
    except Exception:
        client.create_index("opendata", {"primaryKey": "id"})
    index = client.index("opendata")
    res = index.add_documents(docs)
    print("Indexed", len(docs), "documents to Meilisearch. Update ID:", res.get("updateId"))
else:
    print("Meilisearch not available, indexing to local SQLite fallback.")
    sql_index.index_docs(docs)
    print("Indexed", len(docs), "documents to SQLite.")
