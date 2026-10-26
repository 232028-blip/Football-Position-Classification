# Football Position Classification

A local Flask and Angular application for the existing EA Sports FIFA **position classification** project. The fitted Random Forest or XGBoost model classifies one player snapshot as Defender, Forward, Goalkeeper, or Midfielder. Future edition rating prediction is a separate research idea and is not implemented here.

## Data and model

- Source: [Stefano Leone's FIFA 23 complete player dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-23-complete-player-dataset), using the project's 2015–2023 male-player CSV.
- Existing training script: `football_position_classification.py` (41 numeric inputs, player-grouped split, Random Forest and XGBoost).
- The form permits absent Goalkeeping Speed and Mentality Composure ratings; the saved imputer fills them as in training.
- The training script exports `backend/models/model_bundle.joblib` with its fitted preprocessing pipeline, position encoder and exact input order.
- The full CSV and fitted model are deliberately excluded from Git. The downloadable lab package includes both for local use; a fresh GitHub clone requires the CSV and a training run to recreate its fitted model. Commit only the included numerical sample row and JSON payload.

## Run locally

Use Python 3.12, a [Node.js version supported by Angular 22](https://angular.dev/reference/versions), and npm. Open this existing repository in VS Code. Run in PowerShell at the repository root:

```powershell
py -0p
py -3.12 -m venv .venv
& ".\.venv\Scripts\python.exe" -m pip install -r backend/requirements.txt
```

If `py -3.12` is unavailable, check the interpreters reported by `py -0p`. The pinned XGBoost 3.4.1 requires Python 3.12 or newer; Python 3.11 will not install these requirements. The included model was created on Python 3.12, and cross-version loading has not been verified. The lab package already includes the CSV at `data/FIFA_Male_Players_2015_2023.csv` and a bundle at `backend/models/model_bundle.joblib`, so retraining is optional if the bundle loads in your compatible environment.

```powershell
& ".\.venv\Scripts\python.exe" football_position_classification.py --experiment baseline
& ".\.venv\Scripts\python.exe" backend/make_payload.py
& ".\.venv\Scripts\python.exe" backend/test_pipeline.py
& ".\.venv\Scripts\python.exe" -m pytest -q tests/test_utils.py backend/tests
```

In **Terminal 1**, from the root, run `& ".\.venv\Scripts\python.exe" backend/app.py` and keep it open. In **Terminal 2**:

```powershell
cd frontend
npm ci
npm run start -- --proxy-config proxy.conf.json
```

Open [http://localhost:4200](http://localhost:4200), click **Fill sample player**, then **Run local prediction**. The dev proxy forwards `/api/predict` to local Flask on port 5000. Terminal 3 can run `npm run build` in `frontend`.

## GitHub lab

The existing repository is already initialized and has an `origin` remote. New workflows in `.github/workflows/ci.yml` and `.github/workflows/pages.yml` run on a push to `main`; Pages must be configured under **Settings → Pages → Source: GitHub Actions**. The expected static site URL is [232028-blip.github.io/Football-Position-Classification/](https://232028-blip.github.io/Football-Position-Classification/).

GitHub Actions checks source/feature alignment and builds Angular. It does not run model-dependent API tests because the fitted artifact is excluded. GitHub Pages hosts the Angular interface **without a Python server** and disables prediction there. Local API results and CI coverage are described in [the technical report](docs/technical_report.md). Keep the original `GITHUB_LAB_STEPS.md` for the earlier collaboration lab.
