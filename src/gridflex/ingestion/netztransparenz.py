from __future__ import annotations

from pathlib import Path

import pandas as pd


def read_netztransparenz_csv(
    path: str | Path,
    *,
    timestamp_column: str,
    value_column: str,
    value_name: str,
    timezone: str = "Europe/Berlin",
) -> pd.DataFrame:
    """Schema-mapped CSV reader: portal labels must be supplied, never guessed."""
    frame = pd.read_csv(path, sep=None, engine="python", decimal=",")
    missing = {timestamp_column, value_column} - set(frame.columns)
    if missing:
        raise ValueError(f"Source schema changed; missing columns: {sorted(missing)}")
    timestamps = pd.to_datetime(frame[timestamp_column], dayfirst=True, errors="raise")
    if timestamps.dt.tz is None:
        timestamps = timestamps.dt.tz_localize(timezone, ambiguous="infer", nonexistent="raise")
    values = pd.to_numeric(frame[value_column], errors="raise")
    result = pd.DataFrame({value_name: values.to_numpy()}, index=timestamps.dt.tz_convert("UTC"))
    result.index.name = "timestamp_utc"
    return result.sort_index()
