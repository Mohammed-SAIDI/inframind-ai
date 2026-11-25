from fastapi import FastAPI, status
from typing import Dict, Any, List
from .anomaly_engine import AnomalyDetector
from .llm_advisor import LLMAdvisor
app = FastAPI(
    title="InfraMind AI - AIOps SOC Engine",
    description="Microservice AIOps de Réduction du Bruit & Triage d'Alertes (Isolation Forest + Inférence Réelle TinyLlama)",
    version="1.0.0",
    contact={
        "name": "Mohammed SAIDI",
        "url": "https://www.linkedin.com/in/mohammed-saidi-413a9b366/",
    }
)
detector = AnomalyDetector()
advisor = LLMAdvisor()
MAX_HISTORY_ENTRIES = 100
processed_alerts_history: List[Dict[str, Any]] = []
@app.get("/", tags=["Health"])
def healthcheck():
    return {
        "engine": "InfraMind AI",
        "status": "operational",
        "tier1_ml": "Isolation Forest (scikit-learn)",
        "tier2_llm": f"Local Ollama ({advisor.model})",
        "buffered_alerts_count": len(processed_alerts_history)
    }
@app.post("/api/v1/ingest", status_code=status.HTTP_200_OK, tags=["Ingestion"])
def ingest_alert(alert_payload: Dict[str, Any]):
    is_anomaly, score = detector.predict(alert_payload)
    
    if is_anomaly:
        remediation_playbook = advisor.analyze_alert(alert_payload, score)
    else:
        remediation_playbook = "Alerte filtrée (bruit opérationnel normal - aucune action requise)."
    record = {
        "event_id": alert_payload.get("id", len(processed_alerts_history) + 1),
        "rule_id": alert_payload.get("rule", {}).get("id", "N/A"),
        "rule_level": alert_payload.get("rule", {}).get("level", 0),
        "rule_description": alert_payload.get("rule", {}).get("description", "Alerte non qualifiée"),
        "is_anomaly": is_anomaly,
        "anomaly_score": round(score, 4),
        "remediation_advisor": remediation_playbook
    }
    if len(processed_alerts_history) >= MAX_HISTORY_ENTRIES:
        processed_alerts_history.pop(0)
    processed_alerts_history.append(record)
    return record
@app.get("/api/v1/alerts", tags=["Telemetry"])
def get_alerts(limit: int = 50):
    safe_limit = min(limit, MAX_HISTORY_ENTRIES)
    return processed_alerts_history[-safe_limit:]
