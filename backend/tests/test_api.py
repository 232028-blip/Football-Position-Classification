"""Model-dependent checks run locally after baseline training."""

import json
from pathlib import Path

from backend.app import FEATURES, app

ROOT = Path(__file__).resolve().parents[2]
PAYLOAD = json.loads((ROOT / "backend" / "test_payload.json").read_text(encoding="utf-8"))


def test_health():
    response = app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["features"] == len(FEATURES)


def test_predict_valid():
    response = app.test_client().post("/predict", json=PAYLOAD)
    assert response.status_code == 200, response.get_json()
    data = response.get_json()
    assert data["prediction"] in data["classes"]
    assert len(data["probabilities"]) == len(data["classes"])


def test_predict_missing_feature():
    incomplete = dict(PAYLOAD)
    incomplete.pop(FEATURES[0])
    response = app.test_client().post("/predict", json=incomplete)
    assert response.status_code == 400


def test_predict_invalid_json():
    response = app.test_client().post("/predict", data="not-json", content_type="application/json")
    assert response.status_code == 400


def test_predict_outside_supported_range():
    invalid = dict(PAYLOAD)
    invalid["age"] = -1
    response = app.test_client().post("/predict", json=invalid)
    assert response.status_code == 400


def test_missing_goalkeeper_speed_is_imputed():
    outfield = dict(PAYLOAD)
    outfield["goalkeeping_speed"] = None
    response = app.test_client().post("/predict", json=outfield)
    assert response.status_code == 200, response.get_json()
