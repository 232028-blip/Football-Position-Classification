"""FIFA position classification adapted from the project notebook."""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import time
import sklearn
import xgboost


from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import LabelEncoder, label_binarize
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils.class_weight import compute_sample_weight

from xgboost import XGBClassifier
from utils import POSITION_MAPPING, get_position_group

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)

print("Scikit-learn version:", sklearn.__version__)
print("XGBoost version:", xgboost.__version__)

import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Classify FIFA player positions")
parser.add_argument(
    "--experiment",
    choices=("baseline", "rf-depth-16"),
    default="baseline",
    help="Name of the recorded experiment (default: baseline)",
)
EXPERIMENT = parser.parse_args().experiment

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "FIFA_Male_Players_2015_2023.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"
MODEL_DIR = PROJECT_ROOT / "models"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODEL_DIR / "football_position_classifier.pkl"

if not DATA_PATH.is_file():
    raise FileNotFoundError(f"Place the dataset at {DATA_PATH}")

df = pd.read_csv(DATA_PATH, low_memory=False)

print("Dataset shape:", df.shape)
print("Number of records:", df.shape[0])
print("Number of columns:", df.shape[1])

print(df.head().to_string())

df.info()

missing_values = (
    df.isnull()
      .sum()
      .sort_values(ascending=False)
)

print(missing_values[missing_values > 0].head(20).to_string())

print("Duplicate rows:", df.duplicated().sum())
print("Unique players:", df["player_id"].nunique())

df["primary_position"] = (
    df["player_positions"]
    .str.split(",")
    .str[0]
    .str.strip()
)

df["position_group"] = df["primary_position"].map(get_position_group)

df = df.dropna(
    subset=["position_group", "player_id"]
).copy()

print(df["position_group"].value_counts())

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="position_group",
    order=df["position_group"].value_counts().index,
    color="steelblue"
)

plt.title("Distribution of Football Position Groups")
plt.xlabel("Position Group")
plt.ylabel("Number of Records")
plt.xticks(rotation=15)
plt.savefig(OUTPUT_DIR / f"{EXPERIMENT}_position_distribution.png", dpi=150, bbox_inches="tight")
plt.close()

FEATURES = [
    # Personal and general attributes
    "age",
    "height_cm",
    "weight_kg",
    "weak_foot",
    "skill_moves",
    "international_reputation",

    # Attacking
    "attacking_crossing",
    "attacking_finishing",
    "attacking_heading_accuracy",
    "attacking_short_passing",
    "attacking_volleys",

    # Skills
    "skill_dribbling",
    "skill_curve",
    "skill_fk_accuracy",
    "skill_long_passing",
    "skill_ball_control",

    # Movement
    "movement_acceleration",
    "movement_sprint_speed",
    "movement_agility",
    "movement_reactions",
    "movement_balance",

    # Power
    "power_shot_power",
    "power_jumping",
    "power_stamina",
    "power_strength",
    "power_long_shots",

    # Mentality
    "mentality_aggression",
    "mentality_interceptions",
    "mentality_positioning",
    "mentality_vision",
    "mentality_penalties",
    "mentality_composure",

    # Defending
    "defending_marking_awareness",
    "defending_standing_tackle",
    "defending_sliding_tackle",

    # Goalkeeping
    "goalkeeping_diving",
    "goalkeeping_handling",
    "goalkeeping_kicking",
    "goalkeeping_positioning",
    "goalkeeping_reflexes",
    "goalkeeping_speed"
]

print("Selected input features:", len(FEATURES))

assert len(FEATURES) >= 35, "The feature requirement is not satisfied."

X = df[FEATURES].apply(
    pd.to_numeric,
    errors="coerce"
)

target_encoder = LabelEncoder()
y = target_encoder.fit_transform(df["position_group"])

groups = df["player_id"].astype(str)

print("Input shape:", X.shape)
print("Target shape:", y.shape)
print("Target classes:", target_encoder.classes_)
print("Missing feature cells:", X.isnull().sum().sum())

splitter = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

train_index, test_index = next(
    splitter.split(X, y, groups=groups)
)

X_train = X.iloc[train_index]
X_test = X.iloc[test_index]

y_train = y[train_index]
y_test = y[test_index]

groups_train = groups.iloc[train_index]
groups_test = groups.iloc[test_index]

print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Training percentage:", len(X_train) / len(X) * 100)
print("Testing percentage:", len(X_test) / len(X) * 100)

shared_players = set(groups_train).intersection(set(groups_test))

print("Players appearing in both sets:", len(shared_players))

assert len(shared_players) == 0, "Player leakage detected!"

random_forest_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="median",
            add_indicator=True
        )
    ),
    (
        "model",
        RandomForestClassifier(
            n_estimators=250,
            max_depth=20,
            min_samples_leaf=2,
            max_features="sqrt",
            class_weight="balanced_subsample",
            random_state=42,
            n_jobs=-1
        )
    )
])

xgboost_pipeline = Pipeline([
    (
        "imputer",
        SimpleImputer(
            strategy="median",
            add_indicator=True
        )
    ),
    (
        "model",
        XGBClassifier(
            objective="multi:softprob",
            num_class=len(target_encoder.classes_),
            n_estimators=300,
            learning_rate=0.08,
            max_depth=7,
            min_child_weight=3,
            subsample=0.80,
            colsample_bytree=0.80,
            reg_alpha=0.10,
            reg_lambda=1.50,
            tree_method="hist",
            eval_metric="mlogloss",
            random_state=42,
            n_jobs=-1
        )
    )
])

models = {
    "Random Forest": random_forest_pipeline,
    "XGBoost": xgboost_pipeline
}

# The branch comparison requires a real source-code change to max_depth.
rf_depth = models["Random Forest"].named_steps["model"].max_depth
expected_depth = {"baseline": 20, "rf-depth-16": 16}[EXPERIMENT]
if rf_depth != expected_depth:
    raise ValueError(
        f"{EXPERIMENT} requires Random Forest max_depth={expected_depth}; "
        f"the script currently uses {rf_depth}."
    )

training_times = {}

# Random Forest
start_time = time.time()

models["Random Forest"].fit(
    X_train,
    y_train
)

training_times["Random Forest"] = time.time() - start_time

print(
    "Random Forest training time:",
    round(training_times["Random Forest"], 2),
    "seconds"
)

xgb_sample_weights = compute_sample_weight(
    class_weight="balanced",
    y=y_train
)

start_time = time.time()

models["XGBoost"].fit(
    X_train,
    y_train,
    model__sample_weight=xgb_sample_weights
)

training_times["XGBoost"] = time.time() - start_time

print(
    "XGBoost training time:",
    round(training_times["XGBoost"], 2),
    "seconds"
)

results = []
predictions = {}
probabilities = {}

for model_name, model in models.items():

    y_pred = model.predict(X_test)
    y_probability = model.predict_proba(X_test)

    predictions[model_name] = y_pred
    probabilities[model_name] = y_probability

    results.append({
        "Model": model_name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision Macro": precision_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0
        ),
        "Recall Macro": recall_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0
        ),
        "F1 Macro": f1_score(
            y_test,
            y_pred,
            average="macro",
            zero_division=0
        ),
        "ROC-AUC Macro OVR": roc_auc_score(
            y_test,
            y_probability,
            multi_class="ovr",
            average="macro"
        ),
        "Training Time": training_times[model_name]
    })

comparison = (
    pd.DataFrame(results)
    .set_index("Model")
    .sort_values("F1 Macro", ascending=False)
)

print(comparison.round(4).to_string())

# Record measured model metrics for GitHub's baseline/revised comparison.
current_results = comparison.reset_index().copy()
current_results.insert(0, "Experiment", EXPERIMENT)
current_results["Dataset Records"] = len(df)
current_results["Train Records"] = len(X_train)
current_results["Test Records"] = len(X_test)
current_results["Random Seed"] = 42
current_results["RF Max Depth"] = rf_depth
results_path = OUTPUT_DIR / "model_results.csv"
if results_path.exists():
    previous_results = pd.read_csv(results_path)
    all_results = pd.concat([previous_results, current_results], ignore_index=True)
    all_results = all_results.drop_duplicates(
        subset=["Experiment", "Model"], keep="last"
    )
else:
    all_results = current_results
all_results.to_csv(results_path, index=False)
print(f"Saved measured results to {results_path}")

for model_name, y_pred in predictions.items():

    print("\n", "=" * 60)
    print(model_name)
    print("=" * 60)

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=target_encoder.classes_,
            digits=4,
            zero_division=0
        )
    )

overfitting_results = []

for model_name, model in models.items():

    train_prediction = model.predict(X_train)
    test_prediction = predictions[model_name]

    train_accuracy = accuracy_score(
        y_train,
        train_prediction
    )

    test_accuracy = accuracy_score(
        y_test,
        test_prediction
    )

    train_f1 = f1_score(
        y_train,
        train_prediction,
        average="macro"
    )

    test_f1 = f1_score(
        y_test,
        test_prediction,
        average="macro"
    )

    overfitting_results.append({
        "Model": model_name,
        "Train Accuracy": train_accuracy,
        "Test Accuracy": test_accuracy,
        "Accuracy Gap": train_accuracy - test_accuracy,
        "Train F1 Macro": train_f1,
        "Test F1 Macro": test_f1,
        "F1 Gap": train_f1 - test_f1
    })

overfitting_table = (
    pd.DataFrame(overfitting_results)
    .set_index("Model")
)

print(overfitting_table.round(4).to_string())

current_gaps = overfitting_table.reset_index().copy()
current_gaps.insert(0, "Experiment", EXPERIMENT)
gaps_path = OUTPUT_DIR / "overfitting_results.csv"
if gaps_path.exists():
    previous_gaps = pd.read_csv(gaps_path)
    all_gaps = pd.concat([previous_gaps, current_gaps], ignore_index=True)
    all_gaps = all_gaps.drop_duplicates(
        subset=["Experiment", "Model"], keep="last"
    )
else:
    all_gaps = current_gaps
all_gaps.to_csv(gaps_path, index=False)
print(f"Saved train/test gaps to {gaps_path}")

for model_name, row in overfitting_table.iterrows():

    if row["Accuracy Gap"] > 0.05 or row["F1 Gap"] > 0.05:
        print(model_name, ": Possible overfitting—review model complexity.")
    else:
        print(model_name, ": No strong overfitting signal in this split.")

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

for axis, (model_name, y_pred) in zip(
    axes,
    predictions.items()
):

    matrix = confusion_matrix(y_test, y_pred)

    sns.heatmap(
        matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=target_encoder.classes_,
        yticklabels=target_encoder.classes_,
        ax=axis
    )

    axis.set_title(f"{model_name} Confusion Matrix")
    axis.set_xlabel("Predicted Position")
    axis.set_ylabel("Actual Position")

plt.tight_layout()
plt.savefig(OUTPUT_DIR / f"{EXPERIMENT}_confusion_matrices.png", dpi=150, bbox_inches="tight")
plt.close()

number_of_classes = len(target_encoder.classes_)

y_test_binary = label_binarize(
    y_test,
    classes=np.arange(number_of_classes)
)

plt.figure(figsize=(9, 7))

for model_name, y_probability in probabilities.items():

    fpr, tpr, _ = roc_curve(
        y_test_binary.ravel(),
        y_probability.ravel()
    )

    micro_auc = auc(fpr, tpr)

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"{model_name} (Micro AUC = {micro_auc:.4f})"
    )

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    color="black",
    label="Random classifier"
)

plt.title("Multiclass ROC Curve Comparison")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig(OUTPUT_DIR / f"{EXPERIMENT}_roc_curves.png", dpi=150, bbox_inches="tight")
plt.close()

best_model_name = comparison["F1 Macro"].idxmax()
best_pipeline = models[best_model_name]

print("Selected model:", best_model_name)
print(
    "Test Macro F1:",
    comparison.loc[best_model_name, "F1 Macro"]
)

model_bundle = {
    "pipeline": best_pipeline,
    "feature_columns": FEATURES,
    "target_encoder": target_encoder,
    "position_mapping": POSITION_MAPPING,
    "model_name": best_model_name,
    "sklearn_version": sklearn.__version__,
    "xgboost_version": xgboost.__version__,
    "dataset_source": (
        "https://www.kaggle.com/datasets/"
        "stefanoleone992/fifa-23-complete-player-dataset"
    )
}

joblib.dump(model_bundle, MODEL_PATH)

print("Model saved successfully:")
print(MODEL_PATH)

loaded_bundle = joblib.load(MODEL_PATH)

loaded_pipeline = loaded_bundle["pipeline"]
loaded_encoder = loaded_bundle["target_encoder"]
loaded_features = loaded_bundle["feature_columns"]

sample_player = X_test.iloc[[0]][loaded_features]

predicted_code = loaded_pipeline.predict(sample_player)[0]
predicted_position = loaded_encoder.inverse_transform(
    [predicted_code]
)[0]

actual_position = loaded_encoder.inverse_transform(
    [y_test[0]]
)[0]

print("Predicted position:", predicted_position)
print("Actual position:", actual_position)
