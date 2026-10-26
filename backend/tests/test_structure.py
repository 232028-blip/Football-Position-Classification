"""Portable CI check when the local trained model is excluded from Git."""

import ast
from pathlib import Path
import re


def test_application_sources_exist():
    root = Path(__file__).resolve().parents[2]
    for name in (
        "backend/app.py", "frontend/package.json", "frontend/src/app/feature-schema.ts",
        "frontend/src/app/prediction.service.ts", "README.md",
    ):
        assert (root / name).is_file(), name


def test_frontend_feature_names_match_training_script():
    root = Path(__file__).resolve().parents[2]
    tree = ast.parse((root / "football_position_classification.py").read_text(encoding="utf-8"))
    training_features = next(
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == "FEATURES" for target in node.targets)
    )
    schema = (root / "frontend/src/app/feature-schema.ts").read_text(encoding="utf-8")
    frontend_features = re.findall(r"\bname: '([^']+)'", schema)
    assert frontend_features == training_features
