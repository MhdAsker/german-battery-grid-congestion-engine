from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import requests

BASE = "https://www.smard.de/app/chart_data"


@dataclass
class SmardClient:
    timeout_seconds: int = 60

    def available_timestamps(self, filter_id: int, region: str, resolution: str) -> list[int]:
        url = f"{BASE}/{filter_id}/{region}/index_{resolution}.json"
        response = requests.get(url, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.json()["timestamps"]

    def block(self, filter_id: int, region: str, resolution: str, timestamp: int) -> pd.DataFrame:
        url = f"{BASE}/{filter_id}/{region}/{filter_id}_{region}_{resolution}_{timestamp}.json"
        response = requests.get(url, timeout=self.timeout_seconds)
        response.raise_for_status()
        series = response.json()["series"]
        frame = pd.DataFrame(series, columns=["timestamp_ms", "value"])
        frame["timestamp_utc"] = pd.to_datetime(frame.pop("timestamp_ms"), unit="ms", utc=True)
        return frame.set_index("timestamp_utc").sort_index()

