from __future__ import annotations

import pandas as pd


class ValidationError(ValueError):
    pass


def validate_timeseries(
    frame: pd.DataFrame,
    *,
    frequency: str,
    nonnegative: tuple[str, ...] = (),
    allow_missing: bool = True,
) -> dict[str, object]:
    if not isinstance(frame.index, pd.DatetimeIndex) or frame.index.tz is None:
        raise ValidationError("index must be timezone-aware DatetimeIndex")
    if str(frame.index.tz) != "UTC":
        raise ValidationError("canonical index must be UTC")
    if frame.index.has_duplicates:
        raise ValidationError("duplicate timestamps found")
    if not frame.index.is_monotonic_increasing:
        raise ValidationError("timestamps must be sorted")
    for column in nonnegative:
        if (frame[column].dropna() < 0).any():
            raise ValidationError(f"{column} contains negative values")
    expected = pd.date_range(frame.index.min(), frame.index.max(), freq=frequency, tz="UTC")
    missing = expected.difference(frame.index)
    if len(missing) and not allow_missing:
        raise ValidationError(f"{len(missing)} missing intervals")
    return {
        "rows": len(frame), "start": frame.index.min(), "end": frame.index.max(),
        "missing_intervals": len(missing), "nulls": frame.isna().sum().to_dict(),
    }

