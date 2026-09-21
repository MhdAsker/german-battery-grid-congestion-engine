# Assumptions

- Forecast issuance is configured as 10:00 Europe/Berlin on D-1 to align with §13k publication.
- UTC is canonical; local time is derived only for market-day/calendar features.
- A source value is usable only when its evidenced `available_at_utc <= issuance_at_utc`.
- Realized inputs enter only with a conservative lag; current-interval actuals are prohibited.
- The event threshold is a research choice and receives sensitivity analysis.
- Missing means unknown, not zero. Imputation, if modeled, is fit within each training fold.
- Hurdle modeling is selected only after measured zero inflation, not assumed in reported results.
- Battery schedules are counterfactual and use perfect execution within configured constraints.

