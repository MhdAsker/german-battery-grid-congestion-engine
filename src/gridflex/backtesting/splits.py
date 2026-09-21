from __future__ import annotations

import pandas as pd


def expanding_window_splits(index: pd.DatetimeIndex, train_days: int = 365,
                            test_days: int = 30, step_days: int = 30):
    """Yield positional train/test indices without shuffling future into past."""
    start = index.min() + pd.Timedelta(days=train_days)
    while start + pd.Timedelta(days=test_days) <= index.max():
        train = (index < start).nonzero()[0]
        test = ((index >= start) & (index < start + pd.Timedelta(days=test_days))).nonzero()[0]
        if len(train) and len(test):
            yield train, test
        start += pd.Timedelta(days=step_days)
