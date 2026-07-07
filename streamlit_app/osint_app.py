"""Standalone FastAPI service for the OSINT recon engine.

Run this ONLY as a separate HTTP API — Streamlit never imports this module,
so its FastAPI app is never exposed on the Streamlit server.

Start it with either:
    python osint_app.py
    python -m uvicorn osint_app:create_api --factory --host 127.0.0.1 --port 8000
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from recon_engine import perform_recon


class ReconRequest(BaseModel):
    target: str
    lang: str = "en"


def create_api() -> FastAPI:
    """Factory: create and return a FastAPI app instance with routes bound."""
    api = FastAPI(title="OpenData OSINT Core", version="1.0")

    @api.get("/health")
    async def health():
        return {"status": "online"}

    @api.post("/api/v1/recon")
    async def start_recon(request: ReconRequest):
        try:
            return await perform_recon(request.target, request.lang)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))

    return api


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(create_api(), host="127.0.0.1", port=8000)
