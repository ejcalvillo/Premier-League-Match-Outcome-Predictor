# Premier League Match Outcome Predictor

A machine learning project that predicts Premier League match outcomes (home win / draw / away win) from historical match data, with a Streamlit dashboard for interactive predictions and model evaluation.

[Live Demo →](https://premier-league-match-outcome-predictor.streamlit.app/)

## Team project

This was built by a 4-person team as part of a course/portfolio project. Contributions were collaborative across the data pipeline, feature engineering, modeling, and the dashboard — this repo reflects the team's combined work, not one person's individual output.

## Tech stack

- **Python** — pandas, NumPy
- **Modeling** — scikit-learn (Random Forest), XGBoost, CatBoost
- **Evaluation** — TimeSeriesSplit cross-validation, isotonic probability calibration
- **Dashboard** — Streamlit, Plotly
- **Data** — historical Premier League match results, betting odds, and expected goals (xG), scraped from public sources (football-data.co.uk, FBref)

## How it works

**Feature engineering** (28 features per match): rolling form stats computed from each team's prior 5 matches (goals scored/conceded, shots, shots on target, fouls, corners, yellow cards, expected goals), an ELO rating for each team updated match-by-match, normalized bookmaker implied win/draw/loss probabilities, and derived difference features (ELO difference, rolling goals/xG differences). All rolling stats are shifted so a match's features only use information available *before* that match — team identity itself is not used as a feature.

**Model**: a Random Forest classifier (scikit-learn) is the primary model used for live predictions in the dashboard, wrapped in isotonic-calibrated probabilities (`CalibratedClassifierCV`) for better-behaved win/draw/loss probability estimates. XGBoost and CatBoost models are also trained on the same features for comparison.

**Evaluation**: models are compared using 10-fold `TimeSeriesSplit` cross-validation (respecting match chronology rather than random shuffling) across accuracy, precision, recall, F1, log loss, and Brier score, plus feature importance ranking. The dashboard's Model Performance page reports honest **held-out** metrics: the model is trained only on the first 80% of matches by date and evaluated on the final, unseen 20% — see [Known Limitations](#known-limitations) for why this distinction matters.

## Project structure

```
.
├── data/           # Match results, odds, and xG data (CSV)
├── notebooks/      # Data ingestion, feature engineering, and model training
│   └── Advanced/
│       ├── DataIngest.ipynb      # Historical dataset construction (interactive/exploratory)
│       ├── newwebscrape.ipynb    # Cleans current-season scraped data, adds rolling/ELO features
│       ├── FINALMODELS.ipynb     # Trains and evaluates RF/XGBoost/CatBoost, saves models/*.pkl
│       └── predictmatch.ipynb    # Generates features for and predicts upcoming fixtures
├── models/         # Trained model files (.pkl) and cached evaluation metrics
├── dashboard/      # Streamlit app (Match Predictor + Model Performance pages)
└── requirements.txt
```

## Setup and running

There is a single `requirements.txt` at the repo root covering both the notebooks and the dashboard.

### Dashboard only

```bash
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

Opens at http://localhost:8501. Alternatively, run `./start.sh` from within `dashboard/`, which creates a virtual environment and installs dependencies automatically.

### Dashboard pages

- **Match Predictor** — select two teams from the 2025-26 fixture list and get a win/draw/loss probability breakdown from the trained Random Forest model, plus predicted scoreline, recent form, and a team-stats comparison.
- **Model Performance** — accuracy, precision, recall, F1-score, and a confusion matrix computed on the genuinely held-out test set described above.

The dashboard reads match data from `data/` and trained models from `models/` (`random_forest_model.pkl`, `xgboost_model.pkl`, `catboost_model.pkl`, `feature_names.pkl`, `performance_metrics.json`, `performance_test_predictions.csv`), all produced by `notebooks/Advanced/FINALMODELS.ipynb`. Result encoding used throughout the codebase: `0 = Draw`, `1 = Away Win`, `2 = Home Win`.

### Full pipeline (retraining models)

```bash
pip install -r requirements.txt
```

Then run, in order:
1. `notebooks/Advanced/newwebscrape.ipynb` — cleans the current-season match data
2. `notebooks/Advanced/FINALMODELS.ipynb` — trains models and regenerates `models/*.pkl` and `models/performance_metrics.json`
3. `notebooks/Advanced/predictmatch.ipynb` — generates predictions for upcoming fixtures

`notebooks/Advanced/DataIngest.ipynb` documents how the original historical dataset was assembled but relies on interactive clipboard pastes, so it isn't directly re-runnable — it's kept as a record rather than a pipeline step.

## Known limitations

- **Accuracy is modest**: the Random Forest scores ~58% accuracy on genuinely unseen matches, versus a ~44% baseline of always predicting a home win. Three-way match outcome prediction is a hard problem — bookmaker-implied odds alone rarely exceed 55-60% edge either.
- **Draws are the weakest prediction class**: the model rarely predicts a draw correctly, a common issue in football outcome prediction since draws don't have a clear statistical signature the way clear favorites/underdogs do.
- **Earlier version had a data leakage bug**: a previous version of the dashboard's Model Performance page reported accuracy from a model scored against data it had already been trained on. This has been fixed — see `notebooks/Advanced/FINALMODELS.ipynb`'s held-out evaluation cell — but it's a good reminder to always check that evaluation data is genuinely unseen by the model.
- **Dataset size**: historical training data covers roughly 1,600 matches (a few Premier League seasons), which limits how much signal complex models can extract versus simpler baselines.

## Next steps

- Pin exact dependency versions (the committed models were trained with a newer scikit-learn than some environments may have installed, which triggers non-fatal version-mismatch warnings).
- Explore additional features such as head-to-head history, squad injuries/suspensions, or market movement in betting odds over time.
- Automate the data refresh and retraining pipeline instead of the current manual notebook-by-notebook process.
