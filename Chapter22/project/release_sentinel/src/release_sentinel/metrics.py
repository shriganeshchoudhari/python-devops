import os
from pathlib import Path

METRICS_DIR = Path(os.getenv("RS_METRICS_DIR", "/tmp"))
METRICS_FILE = METRICS_DIR / "release_sentinel.prom"

def write_metric(name: str, value: int, labels: dict | None = None):
    labels = labels or {}
    label_str = ",".join(f'{k}="{v}"' for k, v in labels.items())
    label_block = f"{{{label_str}}}" if label_str else ""

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        f.write(f"# TYPE {name} gauge\n")
        f.write(f"{name}{label_block} {value}\n")
