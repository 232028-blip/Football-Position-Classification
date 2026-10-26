# Football Position Classification Application

## Project and provenance

The input data is the project's `FIFA_Male_Players_2015_2023.csv`, sourced from Stefano Leone's [FIFA 23 complete player dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset). The existing `football_position_classification.py` trains two multiclass models on the first fold of a five-fold player-grouped split. A player ID cannot occur in both the train and test partitions. The target comes from the first entry in `player_positions`, mapped to Defender, Forward, Goalkeeper, or Midfielder. It does not forecast the player's next-edition overall rating.

The training run observed 161,583 rows, 110 original columns, 41 selected numeric predictors, 129,267 training records, and 32,316 test records. The saved local bundle contains the selected fitted pipeline (including the fitted median imputer), the target encoder, the ordered input names, and model/version metadata. The model and full dataset stay local.

## Reproduced baseline

| Model | Test accuracy | Test macro F1 | Test one-versus-rest ROC AUC |
| --- | ---: | ---: | ---: |
| Random Forest | 0.9001 | 0.9118 | 0.9839 |
| XGBoost | 0.9027 | 0.9140 | 0.9852 |

These values come from the repository's existing `output/model_results.csv`. The training code selects XGBoost for the API because its test macro F1 is higher. The single grouped holdout is an evaluation sample, not evidence that overfitting or generalization concerns have been resolved. The EA Sports FIFA ratings are video-game ratings; do not interpret the output as measured real-match performance.

## Input and API

The exact 41 numeric fields appear in `frontend/src/app/feature-schema.ts`, in the same order as the training script and saved bundle. Player-details fields have explicit numeric bounds in both the form and Flask; skill ratings are bounded 0–99. Goalkeeping Speed and Mentality Composure can be null when unavailable, allowing the trained imputer to process the missing ratings. `data/sample_inputs.csv`, `backend/test_payload.json`, and `frontend/public/sample-player.json` contain the same non-identifying player attributes for a working demonstration. The example input should reproduce the same class in the direct script, Flask route and browser.

- `GET /health` reports task and feature count.
- `POST /predict` accepts a JSON object with all 41 feature names, rejects missing/extra and invalid numeric fields, and returns the position group, ordered class labels, and ordered probabilities.
- The Angular development proxy forwards `/api/*` to local Flask.
- GitHub Pages displays only the static form; it never runs the Python model.

## Verification and evidence

In this workspace, the saved pipeline produced a Goalkeeper prediction for the included example; the backend test suite passed, and the Angular build and unit test passed. The local Angular proxy returned the Flask health response and the same Goalkeeper prediction. These local checks should be repeated on the student's Windows machine after installing its compatible dependencies. CI runs the mapping tests and feature-schema/source alignment without loading the untracked model. The local API tests additionally require the fitted bundle. Add your own screenshots here after running Flask and Angular in VS Code, and record the GitHub Actions run URLs and Pages deployment URL after pushing.

## Version and reproducibility notes

Python 3.12, scikit-learn 1.6.1, and XGBoost 3.4.1 were used for the verified local model serialization. Use the same compatible package versions when loading the bundle on Windows. Run the original training script again if a saved artifact cannot be loaded under a different environment. Never load model pickle/joblib files from untrusted sources.

## Limitations

The saved bundle is intentionally not available on the public GitHub runner, so CI cannot claim to test real model inference. GitHub Pages is static and cannot call a Flask process running on somebody else's laptop. Future longitudinal prediction of next-edition player presence and rating change is outside the scope of this lab application.
