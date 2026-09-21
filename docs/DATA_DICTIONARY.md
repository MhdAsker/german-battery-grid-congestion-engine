# Canonical data dictionary

| Field | Type / unit | Meaning |
|---|---|---|
| `timestamp_utc` | tz-aware UTC index | start of delivery interval |
| `source_retrieved_at_utc` | UTC timestamp | immutable acquisition timestamp |
| `available_at_utc` | UTC timestamp | earliest evidenced publication time/version |
| `load_forecast_mw` | float MW | day-ahead total-load forecast |
| `wind_forecast_mw` | float MW | day-ahead wind forecast |
| `solar_forecast_mw` | float MW | day-ahead solar forecast |
| `day_ahead_price_eur_mwh` | float EUR/MWh | DA bidding-zone price, only when timely |
| `net_import_mw` | float MW | imports minus exports; sign recorded in metadata |
| `redispatch_mwh` | float MWh | realized measure energy, lagged when a feature |
| `curtailment_mwh` | float MWh | observed outcome under the selected defensible scope |
| `section13k_forecast_mwh` | float MWh | stated next-day quantity; never treated as actual |
| `relief_region` | string | publisher's load-relief region identifier |
| `storage_generation_ban` | nullable boolean | published §13k storage restriction status |
| `y_event` | 0/1 | `curtailment_mwh > configured threshold` |
| `y_volume_event_mwh` | float/NA | volume where `y_event=1` |

Missing values remain null and carry a quality report; they are not fabricated or zero-filled. Units
and sign conventions are attached at adapter/config level and tested before joining.

