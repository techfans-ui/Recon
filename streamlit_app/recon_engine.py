"""Core OSINT recon engine — pure Python, no web framework imports.

Shared by both the Streamlit UI (`streamlit_ui.py`) and the standalone
FastAPI service (`osint_app.py`). Keeping this free of any ASGI/FastAPI
import is what prevents Streamlit's server from trying to auto-mount an
ASGI app.
"""

import asyncio
import random


# Context-aware mock threat intelligence database, per language.
SOURCE_INTELLIGENCE = {
    "en": {
        "github": {"status": "public repository matches found", "entities": 2, "flag": "INFO"},
        "linkedin": {"status": "professional profile indexed", "entities": 1, "flag": "OK"},
        "twitter": {"status": "3 correlated handles identified", "entities": 3, "flag": "OK"},
        "haveibeenpwned": {"status": "2 data breaches detected!", "entities": 2, "flag": "ALERT"},
        "shodan": {"status": "1 vulnerable host port exposed", "entities": 1, "flag": "ALERT"},
        "crt_sh": {"status": "8 active SSL certificates mapped", "entities": 0, "flag": "OK"},
        "whois": {"status": "registrant record matched", "entities": 1, "flag": "OK"},
        "_default": {"status": "no data trail found", "entities": 0, "flag": "CLEARED"},
    },
    "fr": {
        "github": {"status": "correspondances de dépôts publics trouvées", "entities": 2, "flag": "INFO"},
        "linkedin": {"status": "profil professionnel indexé", "entities": 1, "flag": "OK"},
        "twitter": {"status": "3 identifiants corrélés détectés", "entities": 3, "flag": "OK"},
        "haveibeenpwned": {"status": "2 fuites de données détectées !", "entities": 2, "flag": "ALERT"},
        "shodan": {"status": "1 port hôte vulnérable exposé", "entities": 1, "flag": "ALERT"},
        "crt_sh": {"status": "8 certificats SSL actifs cartographiés", "entities": 0, "flag": "OK"},
        "whois": {"status": "enregistrement du titulaire trouvé", "entities": 1, "flag": "OK"},
        "_default": {"status": "aucune trace de données trouvée", "entities": 0, "flag": "CLEARED"},
    },
}


async def check_source_worker(source_name: str, target: str, delay: float, lang: str = "en"):
    """Simulates highly concurrent, non-blocking asynchronous I/O calls to OSINT endpoints."""
    await asyncio.sleep(delay)

    catalog = SOURCE_INTELLIGENCE.get(lang, SOURCE_INTELLIGENCE["en"])
    result_payload = catalog.get(source_name, catalog["_default"])
    return {"source": source_name, **result_payload}


def build_synthesis(target: str, total_entities: int, lang: str) -> str:
    if lang == "fr":
        return (
            f"RAPPORT DE SYNTHÈSE IA CLAUDE // CIBLE : {target}\n"
            f"L'analyse confirme des nœuds d'identité numérique distribués sur {total_entities} plateformes publiques. "
            f"Exposition critique identifiée dans les indices de la matrice opérationnelle de menaces. "
            f"Action recommandée : isoler les enregistrements compromis et régénérer les jetons d'authentification."
        )
    return (
        f"CLAUDE AI SYNTHESIS REPORT // TARGET: {target}\n"
        f"Analysis confirms distributed digital identity nodes across {total_entities} public platforms. "
        f"Critical exposure identified within operational threat matrix indices. "
        f"Action Recommended: Isolate compromised records and regenerate authentication tokens."
    )


async def perform_recon(target: str, lang: str = "en") -> dict:
    """Core recon engine. Runs all source workers concurrently and builds the report.

    Shared by both the FastAPI route and the Streamlit UI so the app works with or
    without a running HTTP server.
    """
    if not target:
        raise ValueError("Target tracking signature required.")

    lang = lang if lang in SOURCE_INTELLIGENCE else "en"

    # List of open-source intelligence matrices to scan in parallel
    sources = ["github", "linkedin", "twitter", "haveibeenpwned", "shodan", "crt_sh", "whois"]

    # Launch concurrent worker tasks via asyncio gathering engine
    tasks = [
        check_source_worker(src, target, random.uniform(0.3, 1.4), lang)
        for src in sources
    ]
    results = await asyncio.gather(*tasks)

    total_entities = sum(item["entities"] for item in results)
    confidence = "HIGH" if total_entities >= 4 else "MEDIUM"

    return {
        "target": target,
        "scan_results": results,
        "metrics": {
            "entities_found": total_entities,
            "correlations_detected": random.randint(2, 5) if total_entities > 0 else 0,
            "confidence_score": confidence,
        },
        "ai_synthesis": build_synthesis(target, total_entities, lang),
    }
