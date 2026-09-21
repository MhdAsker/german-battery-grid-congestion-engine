from __future__ import annotations

import numpy as np
import pandas as pd


def make_targets(values: pd.Series, threshold_mwh: float) -> pd.DataFrame:
    if threshold_mwh < 0:
        raise ValueError("threshold must be nonnegative")
    result = pd.DataFrame(index=values.index)
    result["y_event"] = (values > threshold_mwh).astype("int8")
    result["y_volume_event_mwh"] = values.where(result.y_event.eq(1))
    return result


def target_diagnostics(values: pd.Series, threshold_mwh: float = 0.1) -> dict[str, object]:
    clean = values.dropna()
    event = clean > threshold_mwh
    runs = event.ne(event.shift()).cumsum()
    durations = event[event].groupby(runs[event]).size()
    return {
        "observations": len(clean),
        "zero_share": float(clean.eq(0).mean()),
        "event_share": float(event.mean()),
        "skew": float(clean.skew()),
        "lag_1_autocorrelation": float(clean.autocorr(1)),
        "event_count": int(event.astype(int).diff().eq(1).sum() + bool(event.iloc[0])),
        "median_event_intervals": float(durations.median()) if len(durations) else np.nan,
        "monthly_mean": clean.groupby(clean.index.month).mean().to_dict(),
    }

