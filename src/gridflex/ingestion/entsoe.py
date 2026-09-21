from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from xml.etree import ElementTree as ET

import pandas as pd
import requests

API_URL = "https://web-api.tp.entsoe.eu/api"
GERMANY_LUXEMBOURG = "10Y1001A1001A82H"


@dataclass
class EntsoeClient:
    """Small transparent ENTSO-E client; raw XML can be archived for revisions."""

    api_key: str | None = None
    timeout_seconds: int = 60

    def __post_init__(self) -> None:
        self.api_key = self.api_key or os.getenv("ENTSOE_API_KEY")
        if not self.api_key:
            raise ValueError("Set ENTSOE_API_KEY; never commit the token")

    @staticmethod
    def _period(value: datetime | pd.Timestamp) -> str:
        return pd.Timestamp(value).tz_convert("UTC").strftime("%Y%m%d%H%M")

    def request(self, **params: str) -> bytes:
        query = {"securityToken": self.api_key, **params}
        response = requests.get(API_URL, params=query, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.content

    def day_ahead_prices(self, start: pd.Timestamp, end: pd.Timestamp) -> bytes:
        return self.request(
            documentType="A44", in_Domain=GERMANY_LUXEMBOURG,
            out_Domain=GERMANY_LUXEMBOURG,
            periodStart=self._period(start), periodEnd=self._period(end),
        )

    def load(self, start: pd.Timestamp, end: pd.Timestamp, *, forecast: bool) -> bytes:
        return self.request(
            documentType="A65", processType="A01" if forecast else "A16",
            outBiddingZone_Domain=GERMANY_LUXEMBOURG,
            periodStart=self._period(start), periodEnd=self._period(end),
        )


def parse_timeseries_xml(payload: bytes, value_name: str = "value") -> pd.DataFrame:
    """Parse ENTSO-E Period/Point series without assuming XML namespace version."""
    root = ET.fromstring(payload)
    rows: list[dict[str, object]] = []
    for period in root.findall(".//{*}Period"):
        start_node = period.find("./{*}timeInterval/{*}start")
        resolution_node = period.find("./{*}resolution")
        if start_node is None or resolution_node is None:
            continue
        start = pd.Timestamp(start_node.text)
        step = pd.Timedelta(resolution_node.text)
        for point in period.findall("./{*}Point"):
            position = int(point.findtext("./{*}position"))
            quantity = point.find("./{*}quantity")
            if quantity is None:
                quantity = point.find("./{*}price.amount")
            if quantity is not None:
                rows.append({"timestamp_utc": start + (position - 1) * step,
                             value_name: float(quantity.text)})
    if not rows:
        raise ValueError("No ENTSO-E points found; inspect and archive the raw response")
    return pd.DataFrame(rows).set_index("timestamp_utc").sort_index()
