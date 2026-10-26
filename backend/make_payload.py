"""Export the checked-in example row as a JSON API request."""

import json
from pathlib import Path

import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
bundle = joblib.load(ROOT / "backend" / "models" / "model_bundle.joblib")
features = bundle["features"]
frame = pd.read_csv(ROOT / "data" / "sample_inputs.csv", nrows=1)
if frame.empty or set(frame.columns) != set(features):
    raise ValueError("Sample CSV must have one row with exactly the trained feature names")
row = frame.loc[0, features]
if row.isna().any():
    raise ValueError("Sample CSV contains missing values")
payload = {name: float(row[name]) for name in features}
output = ROOT / "backend" / "test_payload.json"
output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(f"Created {output} with {len(payload)} model inputs")
