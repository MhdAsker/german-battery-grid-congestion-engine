# Data sources and forecast-time availability

Checked against publisher material on 2026-09-21. Exact fields are validated against downloaded
payloads; undocumented labels are never assumed. “Known at issuance” refers to a 10:00 Europe/Berlin
D-1 operational forecast. Retrieval timestamps must accompany every raw artifact.

| Variable | Publisher / interface | Native resolution | Timezone | Unit | Publication / revision | Forecast? | Known at issuance? |
|---|---|---:|---|---|---|---|---|
| §13k stated curtailment quantity by load-relief region | [Netztransparenz §13k publication](https://www.netztransparenz.de/de-de/Systemdienstleistungen/Betriebsfuehrung/Nutzen-statt-Abregeln/Datenver%C3%B6ffentlichungen-Abregelungsstrommengen), page download / linked WebAPI | 15 min | portal offers/labels local time; normalize to UTC | MW average | daily 10:00 for D+1; archive retrieval | forecast quantity | yes |
| §13k allocated quantity | same as above | 15 min | as published | MW average | daily 10:00 for D+1 | allocation | yes |
| storage generation-ban status | same as above | 15 min | as published | 0/1 | daily 10:00 for D+1 | forecast-period restriction | yes |
| redispatch measures | [Netztransparenz Redispatch](https://www.netztransparenz.de/de-de/Systemdienstleistungen/Betriebsfuehrung/Redispatch), CSV export | measure/day fields vary by export | selectable ME(S)Z/UTC | export-defined MW/MWh | operational/post-event; revisions possible | actual measure | no unless explicitly lagged |
| load / generation / wind / solar actuals | [SMARD download center](https://www.smard.de/home/downloadcenter/download-marktdaten); chart-data URL `https://www.smard.de/app/chart_data/{filter}/{region}/...` | 15 min/hour depending series | epoch timestamps normalized UTC | MW or MWh per source metadata | actuals may be revised | actual | no for target interval |
| day-ahead price | SMARD / ENTSO-E | hourly historically; market time unit may change by period | UTC payload, local market day | EUR/MWh | after DA coupling publication | day-ahead | verify issuance cutoff; 10:00 is generally too early |
| day-ahead total-load forecast | [ENTSO-E REST API](https://web-api.tp.entsoe.eu/api), A65/A01, DE-LU EIC `10Y1001A1001A82H` | market time unit | UTC XML | MW | D-1 before DA gate closure; can update | forecast | only versions timestamped by issuance |
| actual total load | ENTSO-E API, A65/A16 | market time unit | UTC XML | MW | after operation; revisions | actual | no; lag only |
| wind/solar forecast | ENTSO-E API, day-ahead wind/solar generation forecast | market time unit | UTC XML | MW | D-1; can update | forecast | only archived issuance-time version |
| actual generation by type | ENTSO-E API | market time unit | UTC XML | MW | after operation; revisions | actual | no; lag only |
| physical cross-border flow | ENTSO-E API per DE-LU border | market time unit | UTC XML | MW | actual/updated | actual | no contemporaneous use; lag only |

## Source caveats

- §13k data start on 1 October 2024, limiting sample size and regime coverage. They describe the
  instrument's forecast/allocation, not necessarily total realized German renewable curtailment.
- SMARD documents a free CC BY 4.0 download route. Its chart-data interface is used conservatively:
  filter IDs belong in configuration after manual portal verification, not hard-coded guesses.
- ENTSO-E requires a personal security token. The API can return multiple revisions/time series; raw
  XML and retrieval time are necessary to reconstruct what was knowable.
- Power (MW average) becomes energy (MWh) only by multiplying by interval duration in hours.

