from __future__ import annotations

import numpy as np
import pandas as pd


def threshold_value_curve(y_true, probability, *, true_positive_value: float,
                          false_positive_cost: float, false_negative_cost: float,
                          thresholds=None) -> pd.DataFrame:
    thresholds = np.linspace(0, 1, 101) if thresholds is None else thresholds
    y = np.asarray(y_true).astype(bool)
    p = np.asarray(probability)
    rows = []
    for threshold in thresholds:
        predicted = p >= threshold
        tp = int((predicted & y).sum())
        fp = int((predicted & ~y).sum())
        fn = int((~predicted & y).sum())
        rows.append({"threshold": threshold, "tp": tp, "fp": fp, "fn": fn,
                     "net_value": tp * true_positive_value - fp * false_positive_cost
                                  - fn * false_negative_cost})
    return pd.DataFrame(rows)


def value_summary(price_only_eur: float, forecast_eur: float, perfect_eur: float) -> dict[str, float]:
    return {"incremental_forecast_value_eur": forecast_eur - price_only_eur,
            "perfect_information_value_eur": perfect_eur - price_only_eur,
            "imperfection_loss_eur": perfect_eur - forecast_eur}

