"""Call the running local Flask API using the example payload."""

import json
from pathlib import Path

import requests

payload = json.loads((Path(__file__).resolve().parent / "test_payload.json").read_text(encoding="utf-8"))
with requests.Session() as session:
    session.trust_env = False
    response = session.post("http://127.0.0.1:5000/predict", json=payload, timeout=60)
    print("HTTP Status:", response.status_code)
    print("Response:", response.text)
    response.raise_for_status()
print("PASS: API request")
