import pandas as pd
import pytest

pytest.importorskip("cvxpy")

from gridflex.battery import optimize_dispatch
from gridflex.config import BatteryConfig


def test_dispatch_respects_bounds():
    prices = pd.Series([-10.0, 100.0], index=pd.date_range("2025-01-01", periods=2, freq="1h", tz="UTC"))
    config = BatteryConfig(power_mw=1, energy_mwh=1, initial_soc_mwh=0,
        minimum_soc_mwh=0, maximum_soc_mwh=1, charge_efficiency=1,
        discharge_efficiency=1, degradation_eur_per_mwh=0,
        curtailment_value_eur_per_mwh=0)
    result = optimize_dispatch(prices, config)
    assert result.schedule.soc_mwh.between(0, 1).all()
    assert result.objective_eur > 0
