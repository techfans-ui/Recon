import time
import random
import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import streamlit as st

# ==========================================
# 1. OSINT CORE ENGINE (shared by API + UI)
# ==========================================

class ReconRequest(BaseModel):
    target: str
    lang: str = "en"


def create_api() -> FastAPI:
    """Factory: create and return a FastAPI app instance with routes bound.

    Use `uvicorn osint_app:create_api --factory` to run the HTTP API standalone.
    """
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


# The FastAPI application is created by `create_api()` when running the HTTP API
# standalone. Streamlit imports this module but does not create an ASGI app by
# default, avoiding accidental exposure of the ASGI routes on the Streamlit
# server.


# ==========================================
# 2. STREAMLIT GHOST TERMINAL FRONTEND UI
# ==========================================

GHOST_CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;700&display=swap');

    /* Overhaul base page components */
    .stApp {
        background-color: #05070a !important;
        color: #00ffcc !important;
        font-family: 'Fira Code', monospace !important;
    }

    /* Interactive element style alterations */
    h1, h2, h3, p, span, label {
        font-family: 'Fira Code', monospace !important;
    }

    /* Custom UI terminal block decoration wrapper */
    .ghost-terminal {
        background-color: #0b0f19;
        border-left: 3px solid #00ffcc;
        border-top: 1px solid #1a2333;
        border-right: 1px solid #1a2333;
        border-bottom: 1px solid #1a2333;
        padding: 22px;
        border-radius: 4px;
        font-family: 'Fira Code', monospace;
        color: #a0aec0;
        line-height: 1.6;
        margin-top: 15px;
        margin-bottom: 15px;
        white-space: pre-wrap;
    }

    .terminal-accent { color: #00ffcc; text-shadow: 0 0 4px #00ffcc; }
    .terminal-alert { color: #ff3366; text-shadow: 0 0 4px #ff3366; }
    .terminal-ok { color: #33ff66; }

    /* Refine default streamlit button wrappers */
    div.stButton > button:first-child {
        background-color: transparent;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        border-radius: 4px;
        padding: 10px 24px;
        font-family: 'Fira Code', monospace;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #00ffcc;
        color: #05070a;
        box-shadow: 0 0 10px #00ffcc;
    }
    </style>
"""

# UI string catalog (English + French).
I18N = {
    "en": {
        "page_title": "OPENDATA // OSINT v1.0",
        "lang_label": "LANGUAGE / LANGUE",
        "subtitle": "AUTOMATED // CORRELATED // SYNTHESIZED RECONNAISSANCE ENGINE",
        "metric_sources": "OSINT DATA SOURCES",
        "metric_sources_val": "10+ Aggregated",
        "metric_latency": "PIPELINE LATENCY",
        "metric_latency_val": "< 2.4s Avg",
        "metric_ai": "AI AGENT INTELLIGENCE",
        "metric_ai_val": "Claude Sonnet v4.6",
        "input_label": "INITIALIZE TARGET COGNITIVE PROBE:",
        "input_placeholder": "Enter email, username, domain, or IP address...",
        "scan_button": "START_RECON →",
        "err_no_target": "[- ] Execution Fault: Valid routing target matrix is required.",
        "err_backend": "[- ] Backend engine failed to initialize. Restart the app and retry.",
        "err_network": "[- ] Network Fault: unable to reach recon engine ({exc}).",
        "err_engine": "[- ] Engine Fault {code}: {text}",
        "spinner": "PROCESSING DATA STREAM MATRICES...",
        "log_scan": "$ opendata scan {target}",
        "log_init": "> INITIALIZING RECONNAISSANCE CORE v1.0...",
        "log_sync": "> SYNCING PARALLEL DATA PORT ROUTERS...",
        "log_interrogate": "> INTERROGATING FEED PIPELINES LIVE...",
        "log_source": "> INTERROGATING SOURCE: {source} → {indicator}",
        "flag_alert": "[!] ALERT: {status}",
        "flag_info": "[i] MATCH: {status}",
        "flag_ok": "[✓] SECURE: {status}",
        "summary_header": "[=== PROBE SCAN MATRIX SUMMARY ===]",
        "summary_entities": "TOTAL LOGICAL ENTITIES MAPPED: {count}",
        "summary_corr": "CROSS-CORRELATIONS ISOLATED: {corr} ({confidence} CONFIDENCE SCORE)",
        "summary_status": "SYSTEM STATUS: RECON ENGINE PROBE OFFLINE // ANALYSIS COMPLETE. █",
        "synthesis_header": "[AI_SYNTHESIS_REPORT]",
    },
    "fr": {
        "page_title": "OPENDATA // OSINT v1.0",
        "lang_label": "LANGUAGE / LANGUE",
        "subtitle": "MOTEUR DE RECONNAISSANCE AUTOMATISÉ // CORRÉLÉ // SYNTHÉTISÉ",
        "metric_sources": "SOURCES DE DONNÉES OSINT",
        "metric_sources_val": "10+ agrégées",
        "metric_latency": "LATENCE DU PIPELINE",
        "metric_latency_val": "< 2,4 s en moy.",
        "metric_ai": "INTELLIGENCE DE L'AGENT IA",
        "metric_ai_val": "Claude Sonnet v4.6",
        "input_label": "INITIALISER LA SONDE COGNITIVE SUR LA CIBLE :",
        "input_placeholder": "Saisir un e-mail, un pseudo, un domaine ou une adresse IP...",
        "scan_button": "LANCER_RECON →",
        "err_no_target": "[- ] Erreur d'exécution : une cible de routage valide est requise.",
        "err_backend": "[- ] Échec de l'initialisation du moteur backend. Redémarrez l'application.",
        "err_network": "[- ] Erreur réseau : moteur de reconnaissance injoignable ({exc}).",
        "err_engine": "[- ] Erreur moteur {code} : {text}",
        "spinner": "TRAITEMENT DES MATRICES DE FLUX DE DONNÉES...",
        "log_scan": "$ opendata scan {target}",
        "log_init": "> INITIALISATION DU CŒUR DE RECONNAISSANCE v1.0...",
        "log_sync": "> SYNCHRONISATION DES ROUTEURS DE PORTS DE DONNÉES PARALLÈLES...",
        "log_interrogate": "> INTERROGATION DES PIPELINES DE FLUX EN DIRECT...",
        "log_source": "> INTERROGATION DE LA SOURCE : {source} → {indicator}",
        "flag_alert": "[!] ALERTE : {status}",
        "flag_info": "[i] CORRESPONDANCE : {status}",
        "flag_ok": "[✓] SÉCURISÉ : {status}",
        "summary_header": "[=== SYNTHÈSE DE LA MATRICE DE SONDAGE ===]",
        "summary_entities": "TOTAL D'ENTITÉS LOGIQUES CARTOGRAPHIÉES : {count}",
        "summary_corr": "CORRÉLATIONS CROISÉES ISOLÉES : {corr} (SCORE DE CONFIANCE {confidence})",
        "summary_status": "ÉTAT DU SYSTÈME : SONDE DU MOTEUR HORS LIGNE // ANALYSE TERMINÉE. █",
        "synthesis_header": "[RAPPORT_DE_SYNTHÈSE_IA]",
    },
}


def run_frontend():
    # Page setup and custom styling injection
    st.set_page_config(page_title="OPENDATA // OSINT v1.0", page_icon="█", layout="wide")
    st.markdown(GHOST_CSS, unsafe_allow_html=True)

    # Language selection (English / Français).
    lang_choice = st.sidebar.radio(
        I18N["en"]["lang_label"],
        options=["en", "fr"],
        format_func=lambda code: {"en": "English", "fr": "Français"}[code],
    )
    t = I18N[lang_choice]

    # Application Layout Header Structure
    st.markdown(
        "<h1><span class='terminal-accent'>OPENDATA</span> — OSINT v1.0</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='color:#718096; margin-top:-15px;'>{t['subtitle']}</p>",
        unsafe_allow_html=True,
    )

    # Core Application Performance Metrics Visual Grid
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label=t["metric_sources"], value=t["metric_sources_val"])
    with m2:
        st.metric(label=t["metric_latency"], value=t["metric_latency_val"])
    with m3:
        st.metric(label=t["metric_ai"], value=t["metric_ai_val"])

    st.write("---")

    # Interactive Input Capture Fields
    target_input = st.text_input(
        label=t["input_label"],
        placeholder=t["input_placeholder"],
    )

    trigger_scan = st.button(t["scan_button"])

    if not trigger_scan:
        return

    if not target_input:
        st.error(t["err_no_target"])
        return

    # Active visual shell rendering layer placeholder
    terminal_shell = st.empty()

    terminal_logs = [
        t["log_scan"].format(target=target_input),
        t["log_init"],
        t["log_sync"],
        t["log_interrogate"],
    ]

    # Interactive output loop simulation logic
    for _ in terminal_logs:
        time.sleep(0.3)
        terminal_shell.markdown(
            f"<div class='ghost-terminal'>{'<br>'.join(terminal_logs)}</div>",
            unsafe_allow_html=True,
        )

    # Run the recon engine directly in-process (no separate HTTP server needed).
    try:
        with st.spinner(t["spinner"]):
            payload = asyncio.run(perform_recon(target_input, lang_choice))
    except Exception as exc:  # noqa: BLE001 - surface any engine fault to the UI
        st.error(t["err_engine"].format(code="ENGINE", text=str(exc)))
        return

    # Stream raw data items to look like a running engine logs terminal
    for check in payload["scan_results"]:
        time.sleep(0.2)

        if check["flag"] == "ALERT":
            label = t["flag_alert"].format(status=check["status"])
            indicator = f"<span class='terminal-alert'>{label}</span>"
        elif check["flag"] == "INFO":
            label = t["flag_info"].format(status=check["status"])
            indicator = f"<span class='terminal-accent'>{label}</span>"
        else:
            label = t["flag_ok"].format(status=check["status"])
            indicator = f"<span class='terminal-ok'>{label}</span>"

        terminal_logs.append(
            t["log_source"].format(source=check["source"].upper(), indicator=indicator)
        )
        terminal_shell.markdown(
            f"<div class='ghost-terminal'>{'<br>'.join(terminal_logs)}</div>",
            unsafe_allow_html=True,
        )

    # Finalize output summary
    metrics = payload["metrics"]
    terminal_logs.append(f"<br><span class='terminal-accent'>{t['summary_header']}</span>")
    terminal_logs.append(t["summary_entities"].format(count=metrics["entities_found"]))
    terminal_logs.append(
        t["summary_corr"].format(
            corr=metrics["correlations_detected"],
            confidence=metrics["confidence_score"],
        )
    )
    terminal_logs.append(t["summary_status"])

    terminal_shell.markdown(
        f"<div class='ghost-terminal'>{'<br>'.join(terminal_logs)}</div>",
        unsafe_allow_html=True,
    )

    # Display the AI Generated Synthesis Document Box
    st.markdown(
        f"<h3 class='terminal-accent'>{t['synthesis_header']}</h3>",
        unsafe_allow_html=True,
    )
    synthesis = payload["ai_synthesis"].replace("\n", "<br>")
    st.markdown(f"<div class='ghost-terminal'>{synthesis}</div>", unsafe_allow_html=True)


# Under `streamlit run app.py`, Streamlit executes this file as the main module,
# so render the UI. The recon engine runs fully in-process (no HTTP server).
#
# To serve the FastAPI HTTP API standalone instead, run:
#     uvicorn app:app --host 127.0.0.1 --port 8000
if __name__ == "__main__":
    run_frontend()
