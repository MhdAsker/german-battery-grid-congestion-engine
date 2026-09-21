import pandas as pd
import pytest

from gridflex.validation import ValidationError, validate_timeseries


def test_validation_reports_missing_intervals():
    index = pd.date_range("2025-01-01", periods=4, freq="15min", tz="UTC").delete(2)
    report = validate_timeseries(pd.DataFrame({"mw": [1, 2, 3]}, index=index), frequency="15min")
    assert report["missing_intervals"] == 1


def test_validation_rejects_naive_index():
    frame = pd.DataFrame({"mw": [1]}, index=pd.DatetimeIndex(["2025-01-01"]))
    with pytest.raises(ValidationError, match="timezone-aware"):
        validate_timeseries(frame, frequency="15min")

