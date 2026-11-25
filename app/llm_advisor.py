import requests
import json
from typing import Dict, Any
class LLMAdvisor:
    def __init__(self, ollama_url: str = "http://localhost:11434", model: str = "tinyllama"):
        # Utilisation de l'API REST de dialogue officielle d'Ollama
        self.ollama_endpoint = f"{ollama_url}/api/chat"
        self.model = model
        self.http_timeout_seconds = 25.0
    def analyze_alert(self, alert_json: Dict[str, Any], anomaly_score: float) -> str:
        rule_data = alert_json.get("rule", {})
        conn_data = alert_json.get("data", {})
        
        rule_desc = rule_data.get("description", "Security incident detected")
        rule_id = str(rule_data.get("id", "N/A"))
        src_ip = conn_data.get("srcip", "100.100.77.1")
        try:
            # Structure officielle de conversation pour TinyLlama Chat
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are a Blue Team SOC Linux security engineer. "
                            "When an incident is reported, answer in 3 concise bullet points:\n"
                            "- Threat & MITRE Technique\n"
                            "- Severity\n"
                            "- Exact containment command (sudo iptables -I INPUT -s <IP> -j DROP)"
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Incident detected: {rule_desc} (Wazuh Rule ID: {rule_id}). Attacker IP: {src_ip}."
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 140
                }
            }
            response = requests.post(self.ollama_endpoint, json=payload, timeout=self.http_timeout_seconds)
            if response.status_code == 200:
                # Dans /api/chat, la reponse se trouve dans message.content
                generated_text = response.json().get("message", {}).get("content", "").strip()
                if generated_text:
                    return f"[TinyLlama Local Inference | Ollama]\n{generated_text}"
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            pass
        return (
            f"[InfraMind Expert Runbook | Fallback Mode]\n"
            f"- Threat : {rule_desc} (Wazuh Rule ID: {rule_id})\n"
            f"- ML Anomaly Score : {anomaly_score:.4f}\n"
            f"- Source Vector : {src_ip}\n"
            f"- MITRE Technique : Credential Access (T1110)\n"
            f"- Immediate Containment Command : sudo iptables -I INPUT -s {src_ip} -j DROP"
        )
