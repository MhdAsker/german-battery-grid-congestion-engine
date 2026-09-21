from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import ks_2samp


def feature_drift(reference: pd.DataFrame, current: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for column in reference.select_dtypes(include="number"):
        if column not in current:
            continue
        statistic, pvalue = ks_2samp(reference[column].dropna(), current[column].dropna())
        rows.append({"feature": column, "ks_statistic": statistic, "p_value": pvalue,
                     "reference_mean": reference[column].mean(), "current_mean": current[column].mean()})
    return pd.DataFrame(rows).sort_values("ks_statistic", ascending=False)


def rolling_brier(y_true: pd.Series, probability: pd.Series, window: str = "30D") -> pd.Series:
    squared_error = (y_true.astype(float) - probability.astype(float)) ** 2
    return squared_error.rolling(window, min_periods=10).mean().rename("rolling_brier")

