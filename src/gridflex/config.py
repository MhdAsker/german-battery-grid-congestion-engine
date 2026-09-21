from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, model_validator


class BatteryConfig(BaseModel):
    power_mw: float = Field(gt=0)
    energy_mwh: float = Field(gt=0)
    initial_soc_mwh: float = Field(ge=0)
    minimum_soc_mwh: float = Field(ge=0)
    maximum_soc_mwh: float = Field(gt=0)
    charge_efficiency: float = Field(gt=0, le=1)
    discharge_efficiency: float = Field(gt=0, le=1)
    degradation_eur_per_mwh: float = Field(ge=0)
    curtailment_value_eur_per_mwh: float = Field(ge=0)

    @model_validator(mode="after")
    def valid_soc(self) -> "BatteryConfig":
        if not self.minimum_soc_mwh <= self.initial_soc_mwh <= self.maximum_soc_mwh:
            raise ValueError("initial SOC must lie within SOC bounds")
        if self.maximum_soc_mwh > self.energy_mwh:
            raise ValueError("maximum SOC cannot exceed energy capacity")
        return self


def load_config(path: str | Path = "configs/default.yaml") -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)

