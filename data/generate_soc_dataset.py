import pandas as pd
import numpy as np
np.random.seed(42)
n_samples = 3000
# 100% de trafic nominal de routine SOC
levels = np.random.choice([2, 3, 4, 5], size=n_samples, p=[0.45, 0.40, 0.10, 0.05])
src_ports = np.random.randint(32768, 61000, size=n_samples)
dst_ports = np.random.choice([80, 443, 53, 8080], size=n_samples, p=[0.45, 0.45, 0.05, 0.05])
df = pd.DataFrame({
    "rule_level": levels,
    "src_port": src_ports,
    "dst_port": dst_ports,
    "is_privileged_dst": (dst_ports <= 1024).astype(int),
    "is_ephemeral_src": (src_ports >= 32768).astype(int)
})
df.to_csv("data/soc_baseline_telemetry.csv", index=False)
print("[OK] Baseline de normalite generee : data/soc_baseline_telemetry.csv (3000 evenements)")
