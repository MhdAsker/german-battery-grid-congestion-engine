from __future__ import annotations

from dataclasses import dataclass

import cvxpy as cp
import numpy as np
import pandas as pd

from gridflex.config import BatteryConfig


@dataclass
class DispatchResult:
    schedule: pd.DataFrame
    objective_eur: float
    status: str


def optimize_dispatch(
    prices_eur_mwh: pd.Series,
    config: BatteryConfig,
    *,
    opportunity_mwh: pd.Series | None = None,
    opportunity_probability: pd.Series | None = None,
) -> DispatchResult:
    """Counterfactual system-level dispatch, not an asset-specific revenue forecast."""
    prices = prices_eur_mwh.astype(float)
    n = len(prices)
    if n < 1 or prices.isna().any():
        raise ValueError("prices must be a non-empty complete series")
    interval_h = (prices.index[1] - prices.index[0]).total_seconds() / 3600 if n > 1 else 1.0
    opportunity = np.zeros(n) if opportunity_mwh is None else opportunity_mwh.reindex(prices.index).fillna(0).to_numpy()
    probability = np.ones(n) if opportunity_probability is None else opportunity_probability.reindex(prices.index).fillna(0).to_numpy()
    if np.any((probability < 0) | (probability > 1)):
        raise ValueError("opportunity probabilities must be between zero and one")

    charge = cp.Variable(n, nonneg=True)
    discharge = cp.Variable(n, nonneg=True)
    soc = cp.Variable(n + 1)
    absorbed = cp.Variable(n, nonneg=True)
    constraints = [soc[0] == config.initial_soc_mwh]
    constraints += [charge <= config.power_mw, discharge <= config.power_mw]
    constraints += [soc >= config.minimum_soc_mwh, soc <= config.maximum_soc_mwh]
    constraints += [absorbed <= cp.multiply(charge * interval_h, probability), absorbed <= opportunity]
    for t in range(n):
        constraints += [soc[t + 1] == soc[t] + charge[t] * interval_h * config.charge_efficiency
                        - discharge[t] * interval_h / config.discharge_efficiency]
    market_value = cp.sum(cp.multiply(prices.to_numpy(), (discharge - charge) * interval_h))
    flexibility_value = config.curtailment_value_eur_per_mwh * cp.sum(absorbed)
    degradation = config.degradation_eur_per_mwh * cp.sum((charge + discharge) * interval_h)
    problem = cp.Problem(cp.Maximize(market_value + flexibility_value - degradation), constraints)
    problem.solve(solver=cp.CLARABEL)
    if problem.status not in {cp.OPTIMAL, cp.OPTIMAL_INACCURATE}:
        raise RuntimeError(f"battery optimization failed: {problem.status}")
    schedule = pd.DataFrame({"price_eur_mwh": prices, "charge_mw": charge.value,
                             "discharge_mw": discharge.value, "soc_mwh": soc.value[1:],
                             "absorbed_opportunity_mwh": absorbed.value}, index=prices.index)
    return DispatchResult(schedule, float(problem.value), problem.status)

