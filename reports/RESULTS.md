# Reproducible results contract

Empirical charts are generated from measured, held-out results only. Place the following exported
tables in `reports/results/` and run `python scripts/render_results.py`:

| Artifact | Required columns | Figure |
|---|---|---|
| `classification_metrics.csv` | `model`, `split`, `pr_auc`, `brier` | Model comparison |
| `calibration.csv` | `model`, `mean_probability`, `event_rate`, `count` | Reliability curve |
| `quantile_metrics.csv` | `model`, `quantile`, `pinball_loss` | Quantile loss |
| `battery_value.csv` | `strategy`, `objective_eur` | Dispatch value comparison |

The renderer refuses missing, empty or structurally invalid artifacts. This is deliberate: portfolio
graphics must trace back to measured results, not illustrative numbers. Each research export should
also be accompanied by the dataset checksum, source retrieval timestamp, split dates and configuration
used to create it.
