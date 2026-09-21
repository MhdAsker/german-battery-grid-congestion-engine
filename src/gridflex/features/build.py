from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AvailabilitySpec:
    column: str
    available_at_column: str


def enforce_availability(
    frame: pd.DataFrame, specs: list[AvailabilitySpec], issuance_time: pd.Series
) -> pd.DataFrame:
    """Mask values whose recorded publication/retrieval time is after issuance."""
    result = frame.copy()
    for spec in specs:
        available = pd.to_datetime(result[spec.available_at_column], utc=True)
        invalid = available > pd.to_datetime(issuance_time, utc=True)
        result.loc[invalid, spec.column] = np.nan
    return result


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Create contemporaneous forecast features and strictly lagged actual features."""
    out = frame.copy()
    if {"wind_forecast_mw", "solar_forecast_mw"} <= set(out):
        out["renewable_forecast_mw"] = out.wind_forecast_mw + out.solar_forecast_mw
    if {"load_forecast_mw", "renewable_forecast_mw"} <= set(out):
        out["residual_load_forecast_mw"] = out.load_forecast_mw - out.renewable_forecast_mw
    for column in ["wind_forecast_mw", "solar_forecast_mw", "load_forecast_mw"]:
        if column in out:
            out[f"{column}_ramp"] = out[column].diff()
    if "day_ahead_price_eur_mwh" in out:
        out["negative_price"] = (out.day_ahead_price_eur_mwh < 0).astype("int8")
    local = out.index.tz_convert("Europe/Berlin")
    out["hour_sin"] = np.sin(2 * np.pi * local.hour / 24)
    out["hour_cos"] = np.cos(2 * np.pi * local.hour / 24)
    out["weekday"] = local.weekday
    out["month"] = local.month
    if "curtailment_mwh" in out:
        # At D-1 issuance, only D-2 and older outcomes are conservatively assumed final.
        periods_day = 96 if pd.infer_freq(out.index[:10]) == "15min" else 24
        out["curtailment_lag_2d_mwh"] = out.curtailment_mwh.shift(2 * periods_day)
    return out

