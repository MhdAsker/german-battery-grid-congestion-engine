from __future__ import annotations

from pathlib import Path

import pandas as pd

BERLIN = "Europe/Berlin"


def normalize_time_index(
    frame: pd.DataFrame,
    timestamp_col: str,
    *,
    source_timezone: str,
    ambiguous: str | bool = "raise",
    nonexistent: str = "raise",
) -> pd.DataFrame:
    """Return a UTC-indexed frame; DST ambiguity must be resolved explicitly."""
    result = frame.copy()
    ts = pd.to_datetime(result.pop(timestamp_col), errors="raise")
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize(source_timezone, ambiguous=ambiguous, nonexistent=nonexistent)
    result.index = pd.DatetimeIndex(ts.dt.tz_convert("UTC"), name="timestamp_utc")
    return result.sort_index()


def atomic_parquet(frame: pd.DataFrame, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    frame.to_parquet(temporary)
    temporary.replace(path)

