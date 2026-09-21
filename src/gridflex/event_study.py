from __future__ import annotations

import pandas as pd


def event_windows(frame: pd.DataFrame, event_column: str = "curtailment_mwh",
                  threshold: float = 0.1, hours: int = 24) -> dict[pd.Timestamp, pd.DataFrame]:
    active = frame[event_column].gt(threshold)
    starts = frame.index[active & ~active.shift(fill_value=False)]
    delta = pd.Timedelta(hours=hours)
    return {start: frame.loc[start - delta:start + delta].copy() for start in starts}

