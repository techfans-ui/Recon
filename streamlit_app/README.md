# OPENDATA — OSINT v1.0 (Ghost Terminal)

A self-contained OSINT reconnaissance demo: a **FastAPI** async backend embedded
inside a **Streamlit** cyberpunk "Ghost Terminal" frontend. The Streamlit process
boots the FastAPI server in a background thread and talks to it over localhost.

> Demo only. The intelligence sources return mock, context-aware sample data — no
> real network reconnaissance is performed.

## Languages / Langues

The UI and the AI synthesis report are fully bilingual. Use the **LANGUAGE / LANGUE**
selector in the sidebar to switch between **English** and **Français**. The chosen
language is sent to the backend (`lang` field) so terminal logs, source findings,
the scan summary, and the synthesis report are all localized.

## Run locally

```bash
cd streamlit_app
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Streamlit opens at http://localhost:8501. The embedded FastAPI engine runs at
http://127.0.0.1:8000 (see `/health` and `POST /api/v1/recon`).

## How it works

- `run_backend()` hosts FastAPI via uvicorn in a daemon thread.
- `ensure_backend_running()` (cached with `st.cache_resource`) starts it once and
  waits for `/health` before the UI accepts input.
- The UI streams a live terminal log, then renders the AI synthesis report.
