# German Grid Congestion, Curtailment & Storage Opportunity Engine

A reproducible applied energy-data-science project asking whether German next-day
renewable-curtailment/grid-congestion risk is predictable from information genuinely available at
forecast issuance, and whether those forecasts alter a counterfactual flexibility strategy.

> **Research status:** the repository contains the data contracts, ingestion, validation, modeling,
> evaluation and simulation pipeline. It intentionally contains no invented observations or results.
> Results sections remain pending until the public-source snapshot has been acquired and validated.

## Why this matters

Redispatch changes power injections to prevent or resolve network congestion while maintaining the
system balance. Renewable down-regulation is related to, but not synonymous with, negative prices:
prices are bidding-zone signals, whereas congestion is spatial. Germany's growing variable renewable
fleet makes calibrated probability forecasts potentially useful for scheduling flexible demand.

The primary target is observed renewable curtailment where defensible public outcome data exist.
The §13k *Nutzen statt Abregeln* next-day publication is retained as a separately labelled forecast
proxy; it is not silently relabelled as realized curtailment.

## Data

Adapters cover Netztransparenz schema-mapped CSV exports, SMARD's public chart-data interface, and
the authenticated ENTSO-E Transparency REST API. Every canonical row uses UTC; Europe/Berlin is used
for market/calendar interpretation. Raw responses should be stored immutably with retrieval metadata
so revisions can be reproduced. See [data sources](docs/DATA_SOURCES.md),
[dictionary](docs/DATA_DICTIONARY.md), and [assumptions](docs/ASSUMPTIONS.md).

## Research and ML methodology

The workflow deliberately starts with target diagnostics (zero share, skew, seasonality,
autocorrelation and event runs), then benchmarks always-no-event, previous-day, logistic and seasonal
baselines. A hurdle model estimates event probability and event-conditional P10/P50/P90 volume.
Expanding-window backtests report precision, recall, F1, ROC-AUC, PR-AUC, Brier score, calibration,
MAE, RMSE, pinball loss and interval coverage. Optional LightGBM/XGBoost/SHAP comparisons are enabled
by `pip install -e ".[ml]"`. Interpretations describe predictive associations, not causes.

## Storage and forecast value

The convex dispatch model compares price-only, forecast-aware, and perfect-information schedules.
It combines market value, an explicitly configurable value for absorbing otherwise-curtailed energy,
and degradation cost. Threshold value curves expose false-positive and false-negative costs, while
the difference from perfect information measures forecast imperfection loss.

**This is a counterfactual system-level flexibility study. Public aggregated data do not establish
asset-specific electrical connectivity, technical or contractual eligibility, deliverability, or
guaranteed access to/monetization of curtailed MWh.**

## Results and explainability

No empirical result is claimed before a versioned data snapshot passes validation. Once run, generated
metrics, calibration plots, SHAP summaries, event windows and seasonal/drift views belong in
`reports/`; they should record the data hash, retrieval time, split dates and configuration.

## Reproduction

```bash
python -m venv .venv
# activate the environment, then:
pip install -e ".[dev,ml]"
copy .env.example .env              # Windows; add ENTSOE_API_KEY locally
pytest
streamlit run dashboard/app.py
```

Use `gridflex validate data/processed/unified.parquet` and then
`gridflex diagnose-target data/processed/unified.parquet`. Detailed methodology and limitations are
in [METHODOLOGY.md](docs/METHODOLOGY.md) and [LIMITATIONS.md](docs/LIMITATIONS.md).

