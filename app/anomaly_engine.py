import os
import joblib
import numpy as np
from typing import Tuple, Dict, Any
class AnomalyDetector:
    def __init__(self, model_path: str = "models/isolation_forest_soc.joblib", scaler_path: str = "models/robust_scaler.joblib"):
        if not os.path.exists(model_path) or not os.path.exists(scaler_path):
            raise FileNotFoundError("Artefacts MLOps manquants. Lancez d'abord python train_pipeline.py")
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        
        # Seuil operationnel calibre (Baseline SOC normale = ~0.28, seuil d'anomalie = 0.18)
        self.anomaly_threshold = 0.18
    def extract_features(self, alert: Dict[str, Any]) -> np.ndarray:
        rule_meta = alert.get("rule", {})
        data_meta = alert.get("data", {})
        rule_level = float(rule_meta.get("level", 3))
        src_port = float(data_meta.get("srcport", 0) or 0)
        dst_port = float(data_meta.get("dstport", 0) or 0)
        is_privileged_dst = 1.0 if dst_port <= 1024 else 0.0
        is_ephemeral_src = 1.0 if src_port >= 32768 else 0.0
        raw_vector = np.array([[rule_level, src_port, dst_port, is_privileged_dst, is_ephemeral_src]], dtype=np.float64)
        return self.scaler.transform(raw_vector)
    def predict(self, alert: Dict[str, Any]) -> Tuple[bool, float]:
        X_scaled = self.extract_features(alert)
        raw_score = float(self.model.decision_function(X_scaled)[0])
        # Decision 100% Machine Learning basee sur le score d'isolation des arbres
        is_anomaly = (raw_score < self.anomaly_threshold)
        return is_anomaly, raw_score
