import pandas as pd

from gridflex.features import AvailabilitySpec, enforce_availability, make_targets


def test_availability_masks_hindsight():
    frame = pd.DataFrame({"forecast": [1.0, 2.0], "published": pd.to_datetime(
        ["2025-01-01T08:00Z", "2025-01-01T11:00Z"])})
    issuance = pd.Series(pd.to_datetime(["2025-01-01T10:00Z"] * 2))
    result = enforce_availability(frame, [AvailabilitySpec("forecast", "published")], issuance)
    assert result.forecast.notna().tolist() == [True, False]


def test_targets_keep_zero_volume_out_of_conditional_target():
    y = pd.Series([0.0, 0.2])
    result = make_targets(y, 0.1)
    assert result.y_event.tolist() == [0, 1]
    assert pd.isna(result.y_volume_event_mwh.iloc[0])

