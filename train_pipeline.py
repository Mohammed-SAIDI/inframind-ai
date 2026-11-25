import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import RobustScaler
import os
print("\n" + "="*70)
print("[PIPELINE] INFRAMIND AI - ENTRAINEMENT DES ARBRES ISOLATION FOREST")
print("="*70)
df = pd.read_csv("data/soc_baseline_telemetry.csv")
feature_cols = ["rule_level", "src_port", "dst_port", "is_privileged_dst", "is_ephemeral_src"]
X = df[feature_cols].values
scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
# Entrainement pur sur la normalite
model = IsolationForest(
    n_estimators=100,
    contamination=0.01,
    random_state=42,
    n_jobs=-1
)
model.fit(X_scaled)
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/isolation_forest_soc.joblib")
joblib.dump(scaler, "models/robust_scaler.joblib")
print("[SUCCESS] Arbres entraines et modeles sauvegardes.\n")
