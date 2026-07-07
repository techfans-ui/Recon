# OpenData Ghost FR
Scaffolded French OSINT web app (Next.js frontend + FastAPI backend + Meilisearch) — starter workspace.

Quick start (local, requires Docker):

1. Copy `.env.example` to `.env` and edit if needed.
2. Start services:

```bash
docker-compose up --build
```

3. Frontend: http://localhost:3000 — Backend: http://localhost:8000 — Meilisearch: http://localhost:7700

Notes:
- Frontend calls `${NEXT_PUBLIC_API_URL}/search` to query backend.
- Backend attempts to query Meilisearch index `opendata`; if Meilisearch not populated, it returns sample data.
- Replace sample data in `backend/app/data/sample.json` or index real datasets into Meilisearch.

Next steps I can do for you:
- Implement indexing scripts to push CSV/JSON into Meilisearch.
- Add French translations and UI polish to match the OpenData Ghost theme.
- Deploy configuration for Vercel + Render.

Tell me which next step to implement.