# GitHub lab: remaining steps after extracting this ZIP

These steps map to the attached lab manual's Parts A–M. The ZIP already
contains the converted VS Code script, original notebook, actual source CSV,
README, requirements, `.gitignore`, an executable position-mapping unit test,
and the GitHub Actions workflow. The code deliberately retains the baseline
Random Forest `max_depth=20`; make the revised `16` change on a collaborator's
branch so the pull request contains a real, reviewable code improvement.

## A–C. Open and run the existing project

1. Extract the ZIP and use **VS Code → File → Open Folder** to open the inner
   `Football-Position-Classification` directory containing this README.
2. Install Python 3.12 and the VS Code Python extension if necessary. Open
   **Terminal → New Terminal**. The following commands assume PowerShell.
3. Create the virtual environment and install the exact ML-library versions
   recorded from the notebook (scikit-learn 1.6.1 and XGBoost 3.4.1).

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe football_position_classification.py --experiment baseline
```

4. Wait for training to finish. Check `output/model_results.csv` for the two
   *actual* baseline rows. Check the baseline PNG charts. The trained `.pkl`
   stays in `models/` and is excluded from Git. If this ZIP already includes
   measured baseline output from validation, you can still rerun locally to
   verify it on your own system; this replaces the baseline rows in the CSV.
5. In VS Code **Ctrl+Shift+P → Python: Select Interpreter**, select the `.venv`
   interpreter. `git --version` checks your Git installation.

The notebook version is in `notebooks/`. `data/` contains the source CSV for
local training and `.gitignore` excludes it from GitHub. `README.md` records
the Kaggle URL, how to run the script, what the model predicts, and its limits.
The notebook-to-script conversion has already removed Colab-specific `!pip`,
`drive.mount`, `/content/drive`, `files.download`, and cell-only `display`/
`plt.show` calls. The original 41 features and grouped splitting are retained.

## D–F. Create and upload the repository

1. On GitHub use **+ → New repository**. Suggested name:
   `Football-Position-Classification`. Choose your intended visibility. Leave
   **Initialize with README** and **Add .gitignore** unchecked because they
   are already in this directory. Copy the HTTPS repository URL.
2. Run the following from the opened project folder, replacing the URL.

```powershell
git init
git branch -M main
git status
git add .
git status
git diff --cached --stat
git commit -m "Add baseline football position classification project"
git remote add origin https://github.com/YOUR_USERNAME/Football-Position-Classification.git
git push -u origin main
```

3. Before committing, inspect the staged list. It should contain source code,
   original notebook, docs, CI files, and small generated output. It should
   *not* include `data/`, `models/`, `.venv/`, tokens, or secrets. Make sure
   your local `output/model_results.csv` and `output/overfitting_results.csv`
   contain measured baseline values.
   Check the repository's **Code** tab after pushing.
4. Record the baseline version:

```powershell
git tag v1.0
git push origin v1.0
```

## G and L. Collaborator and Issue

1. In repository **Settings → Collaborators**, invite the *real person* doing
   the lab with you. They accept the invitation using their account.
2. In **Issues → New issue**, use the title:
   `Compare Random Forest maximum depth 20 against 16`.
3. Issue body:

```markdown
Keep the same 41 features, source CSV, player-grouped split, random seed,
and XGBoost settings. On a feature branch reduce Random Forest max_depth
from 20 to 16, run both models, commit the revised output/model_results.csv,
and compare accuracy, macro precision, macro recall, macro F1, ROC-AUC, and
train/test gaps with the baseline.
```

Keep the created issue number for the PR description. Additional Issues can
track future tasks, such as checking position-class support or testing saved
model inference; do not mark an unperformed task complete.

## H. Controlled change on the collaborator's branch

The collaborator uses their machine and account:

```powershell
git clone https://github.com/YOUR_USERNAME/Football-Position-Classification.git
cd Football-Position-Classification
git switch -c feature/rf-depth-16
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

The collaborator copies the CSV provided in this ZIP into the cloned
repository's local `data/` directory. Git intentionally does not transfer it.
In `football_position_classification.py`, change only the Random Forest line
`max_depth=20` to `max_depth=16`. The experiment-name check deliberately
rejects `rf-depth-16` until the actual code is changed.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe football_position_classification.py --experiment rf-depth-16
git status
git add football_position_classification.py output/model_results.csv output/overfitting_results.csv output/*.png
git commit -m "Compare Random Forest depth 16 with baseline"
git push -u origin feature/rf-depth-16
```

The revised run adds two rows to each of `output/model_results.csv` and
`output/overfitting_results.csv`, leaving the baseline rows in place.
`Training Time` may differ across machines; compare predictive metrics under
the same recorded split. Confirm that the player-leakage assertion passed.
If a chart file is absent, stage the files that exist rather than assuming
it was saved.

## I–J. Pull request, review, approval, merge

1. Collaborator opens **Pull requests → New pull request** with base `main`
   and compare `feature/rf-depth-16`. Use this description with numbers
   copied from the *actual* CSV:

```markdown
## Change
Reduced Random Forest max_depth from 20 to 16.

## Controlled comparison
Same source CSV, features, grouped split, random seed, and XGBoost settings.

| Metric | Baseline RF | Revised RF |
| --- | ---: | ---: |
| Accuracy | [actual] | [actual] |
| Macro precision | [actual] | [actual] |
| Macro recall | [actual] | [actual] |
| Macro F1 | [actual] | [actual] |
| Macro ROC-AUC OVR | [actual] | [actual] |

Describe the measured train/test gaps and whether the revised model improved.

Closes #ISSUE_NUMBER
```

2. The repository owner reviews **Files changed**, the recorded metrics, and
   the **Python CI** check. They leave a specific review comment, ask for any
   needed correction, approve, and merge. The author and reviewer should use
   their own GitHub accounts; do not claim a review that did not occur.
3. The owner updates their local `main` and tags the reviewed version:

```powershell
git switch main
git pull origin main
git log --oneline --decorate -5
git tag v1.1
git push origin v1.1
```

## K. Record and explain performance

Inspect all four measured rows in `output/model_results.csv`. The fields
include the experiment, model, five evaluation metrics, training time,
dataset/train/test row counts, random seed, and RF depth. Review all four
rows in `output/overfitting_results.csv` too. It is legitimate if the revised
model gets worse; report its actual measured outcome. If a deeper model has
a larger train/test gap, describe that observation, but do not claim that a
single split proves that overfitting is absent or present everywhere.

```powershell
.\.venv\Scripts\python.exe -c "import pandas as pd; d=pd.read_csv('output/model_results.csv'); print(d[['Experiment','Model','Accuracy','Precision Macro','Recall Macro','F1 Macro','ROC-AUC Macro OVR']].to_string(index=False))"
```

Check the repository's commit history and the `v1.0`/`v1.1` tags. If the PR
contained `Closes #ISSUE_NUMBER` with a valid issue number, check that the
Issue was closed after merge.

## M. Automated CI and deliberate fail/fix demonstration

`.github/workflows/python-test.yml` and `tests/test_utils.py` are already
included. CI runs a small real position-mapping test on pushes and PRs; it
does not retrain both ML models on GitHub's runner. The PR check should be
green when the mapping is correct.

For the manual's failing-test demonstration, the owner creates a disposable
`ci-demo` branch after pulling merged `main`:

```powershell
git switch main
git pull origin main
git switch -c ci-demo
```

Temporarily change the `"GK": "Goalkeeper"` entry in `utils.py` to
`"GK": "Forward"` **on `ci-demo` only**. Push the deliberately failing
test, and take a screenshot of the red run in the **Actions** tab:

```powershell
git add utils.py
git commit -m "Demonstrate CI detecting an incorrect position mapping"
git push -u origin ci-demo
```

Then restore the correct mapping, push the fix, and take a screenshot of the
green run. There is no need to merge the deliberately failing branch:

```powershell
git restore --source=main -- utils.py
git add utils.py
git commit -m "Restore correct position mapping"
git push origin ci-demo
```

## Evidence to collect for submission

- VS Code Explorer showing the prepared project and local script running.
- Local unit test passing, and script output showing actual split, metrics,
  model export, and saved baseline and revised CSV rows.
- Repository files and initial baseline commit; the large CSV stays local.
- Issue, collaborator invitation, the collaborator's branch commit, PR diff,
  reviewer comment/approval, merged PR, and commit history.
- Performance comparison with actual CSV values and tags `v1.0`/`v1.1`.
- GitHub Actions green PR test, red demonstration run, and green fixed run.

The saved notebook output alone is not evidence that the converted local
script has run on your own machine. Do not fill the report with invented model
metrics, approval events, or screenshots.
