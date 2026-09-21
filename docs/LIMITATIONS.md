# Limitations

- Public national/TSO aggregates do not locate an asset electrically or prove congestion relief.
- §13k forecasts/allocations are not a long historical realized-curtailment target and begin only in
  October 2024; concept drift and limited statistical power are material.
- Redispatch and renewable curtailment are related but non-identical scopes. Reporting must preserve
  operator, direction, technology, and requested/realized distinctions available in source data.
- Publication timestamps and revisions can make retrospective APIs unsafe for pseudo-real-time work.
- ENTSO-E/SMARD coverage, resolution and bidding-zone definitions change over time.
- SHAP and feature ablations reveal predictive association, not physical or economic causation.
- The battery model excludes network power flow, bids, imbalance exposure, taxes, grid fees,
  qualification, contracts and market impact. Its “curtailment value” is a scenario parameter, not
  guaranteed revenue.
- Performance and value cannot be stated until a validated, versioned data snapshot is evaluated.

