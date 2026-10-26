"""Local inference API for the fitted football position classifier."""

import math
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

BASE = Path(__file__).resolve().parent
BUNDLE_PATH = BASE / "models" / "model_bundle.joblib"
if not BUNDLE_PATH.is_file():
    raise FileNotFoundError(
        f"Fitted model missing: {BUNDLE_PATH}. Run the baseline training script first."
    )

# Load only our own trusted, locally generated artifact; joblib is unsafe for untrusted files.
BUNDLE = joblib.load(BUNDLE_PATH)
MODEL = BUNDLE["pipeline"]
FEATURES = BUNDLE["features"]
ENCODER = BUNDLE["target_encoder"]
CLASSES = [str(value) for value in ENCODER.classes_]
OPTIONAL_RATINGS = {"goalkeeping_speed", "mentality_composure"}

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", features=len(FEATURES), task="position classification")


@app.post("/predict")
def predict():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Expected a JSON object"), 400

    missing = [name for name in FEATURES if name not in data]
    extra = [name for name in data if name not in FEATURES]
    if missing or extra:
        return jsonify(error="Input schema mismatch", missing=missing, extra=extra), 400

    for name in FEATURES:
        value = data[name]
        if value is None and name in OPTIONAL_RATINGS:
            continue  # The saved fitted imputer handles the source data's missing ratings.
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            return jsonify(error="Invalid numeric input", feature=name), 400
        lower, upper = (15, 65) if name == "age" else (
            (100, 230) if name == "height_cm" else (
                (30, 200) if name == "weight_kg" else (
                    (1, 5) if name in {"weak_foot", "skill_moves", "international_reputation"}
                    else (0, 99)
                )
            )
        )
        if not lower <= value <= upper:
            return jsonify(error="Input outside supported range", feature=name), 400

    frame = pd.DataFrame([[data[name] for name in FEATURES]], columns=FEATURES)
    try:
        code = int(MODEL.predict(frame)[0])
        prediction = str(ENCODER.inverse_transform([code])[0])
        result = {
            "prediction": prediction,
            "task": "position classification",
            "classes": CLASSES,
            "model_name": BUNDLE["model_name"],
            "disclaimer": "EA Sports FIFA player attributes; teaching/research prototype.",
        }
        if hasattr(MODEL, "predict_proba"):
            result["probabilities"] = [float(x) for x in MODEL.predict_proba(frame)[0]]
        return jsonify(result)
    except (ValueError, TypeError) as exc:
        return jsonify(error="Invalid input", detail=str(exc)), 400
    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify(error="Prediction processing failed"), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
