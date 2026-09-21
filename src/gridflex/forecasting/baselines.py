from __future__ import annotations

import numpy as np
import pandas as pd


def always_no_event(index: pd.Index) -> pd.Series:
    return pd.Series(0.0, index=index, name="event_probability")


def previous_day_event(y: pd.Series, periods_per_day: int) -> pd.Series:
    return y.shift(periods_per_day).fillna(0).astype(float)


def seasonal_volume_mean(y: pd.Series) -> pd.Series:
    """Expanding hour-of-week mean, shifted to exclude the row being predicted."""
    key = y.index.dayofweek * 24 + y.index.hour
    return y.groupby(key).transform(lambda group: group.expanding().mean().shift())

