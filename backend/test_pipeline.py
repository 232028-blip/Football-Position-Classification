"""Check a sample prediction without starting Flask."""

import json
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
bundle = joblib.load(ROOT / "backend" / "models" / "model_bundle.joblib")
payload = json.loads((ROOT / "backend" / "test_payload.json").read_text(encoding="utf-8"))
features = bundle["features"]
assert set(payload) == set(features)
frame = pd.DataFrame([[payload[name] for name in features]], columns=features)
code = bundle["pipeline"].predict(frame)[0]
print("Prediction:", bundle["target_encoder"].inverse_transform([int(code)])[0])
print("Probabilities:", bundle["pipeline"].predict_proba(frame)[0].tolist())
print("PASS: local inference")
