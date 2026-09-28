# Football Position Classification

This project classifies FIFA player snapshots into **Goalkeeper, Defender,
Midfielder, or Forward** from 41 selected numeric player attributes. It is a
position-classification experiment, not a prediction of a player's future
performance. The source project was an existing Google Colab notebook; the
main script retains its Random Forest and XGBoost settings.

## Dataset

The included `data/FIFA_Male_Players_2015_2023.csv` was provided with this
project. Source stated in the original notebook:
[FIFA 23 complete player dataset on Kaggle](https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset).
The source file has 161,583 records and 110 columns. The script selects 41
inputs and excludes records without a mapped position or player ID. The CSV is
in the ZIP for local use and is ignored by Git because of its size. The
original notebook is kept in `notebooks/` for reference.

## Start in VS Code (Windows PowerShell terminal)

Open **this folder** with VS Code. Select a Python 3.12 interpreter, then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe football_position_classification.py --experiment baseline
```

The first full run trains both models using the same player-grouped split
(`StratifiedGroupKFold`, first fold of five, approximately 80/20). The script
checks that a player ID never occurs in both train and test. It writes actual
model metrics to `output/model_results.csv`, saves charts to `output/`, and
records train/test gaps in `output/overfitting_results.csv`. It saves the
winning trained model to `models/football_position_classifier.pkl`.
The dataset and model stay local when you run `git add .` because `.gitignore`
excludes `data/` and `models/`.

To compare a collaborator's controlled Random Forest change, edit only
`max_depth=20` to `max_depth=16` in the script **on a feature branch**, then:

```powershell
.\.venv\Scripts\python.exe football_position_classification.py --experiment rf-depth-16
```

This appends revised results to the CSV while retaining the baseline results.
The script rejects an experiment label if the source code still uses the wrong
Random Forest depth. The XGBoost settings, features, and random seed are kept
the same. `Training Time` can vary from computer to computer.

## Files

| Path | Purpose |
| --- | --- |
| `football_position_classification.py` | Converted and adapted notebook experiment |
| `utils.py` | Position mapping used by training and CI test |
| `tests/test_utils.py` | Small dataset-free unit test |
| `.github/workflows/python-test.yml` | GitHub Actions CI on pushes and PRs |
| `output/model_results.csv` | Baseline/revised measured metrics after running |
| `output/overfitting_results.csv` | Baseline/revised train/test gap diagnostics |
| `output/*.png` | Generated charts after running |
| `models/*.pkl` | Generated local model, excluded from Git |
| `GITHUB_LAB_STEPS.md` | Repository, Issue, collaborator, branch, PR, review, tag, CI exercise |

## Evaluation and limitations

The script reports accuracy, macro precision, macro recall, macro F1,
multiclass one-vs-rest ROC-AUC, classification reports, confusion matrices,
ROC curves, and train/test metric gaps. A train/test gap is a diagnostic, not
a proof that a model cannot overfit. A single player-grouped fold should not
be presented as a full cross-validation study. Use actual figures from
`output/model_results.csv` when writing the lab report.

## Contributors

- Original author: add your name on GitHub.
- Lab collaborator: add their name after accepting the repository invitation.
