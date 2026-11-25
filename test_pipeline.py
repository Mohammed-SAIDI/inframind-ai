import requests
import json
import time
TARGET_ENDPOINT = "http://127.0.0.1:8000/api/v1/ingest"
# Cas 1 : Trafic bénin de routine (Filtré par Isolation Forest, zéro appel LLM)
benign_sample = {
    "id": "SIM-001",
    "rule": {"id": "31101", "level": 3, "description": "Accès page web statique normale"},
    "data": {"srcip": "192.168.100.50", "srcport": 54210, "dstport": 80}
}
# Cas 2 : Attaque Brute-Force SSH réelle (Wazuh Règle 5710)
ssh_attack_sample = {
    "id": "SIM-002",
    "rule": {"id": "5710", "level": 10, "description": "sshd: Tentative multiple d'authentification échouée (Attaque Brute-Force)"},
    "data": {"srcip": "100.100.77.1", "srcport": 61234, "dstport": 22}
}
# Cas 3 : Injection SQL réelle (Wazuh Règle 31103)
sqli_attack_sample = {
    "id": "SIM-003",
    "rule": {"id": "31103", "level": 13, "description": "SQL Injection attempt detected in HTTP URI parameter"},
    "data": {"srcip": "100.100.77.1", "srcport": 50412, "dstport": 80}
}
def send_alert(title: str, payload: dict):
    print("\n" + "="*70)
    print(f"[TEST] {title}")
    print("="*70)
    start_time = time.time()
    res = requests.post(TARGET_ENDPOINT, json=payload)
    elapsed = time.time() - start_time
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))
    print(f"[METRIC] Latence : {elapsed:.3f} s")
send_alert("1. BRUIT BENIN (Filtrage ML sans charge LLM)", benign_sample)
send_alert("2. ATTAQUE SSH BRUTE-FORCE (Inference Reelle TinyLlama)", ssh_attack_sample)
send_alert("3. ATTAQUE SQL INJECTION CRITIQUE (Filet Deterministe + LLM)", sqli_attack_sample)
print("\n" + "="*70 + "\n")
