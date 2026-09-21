# Methodology

1. Archive raw responses with URL/query (token redacted), retrieval time, checksum and license.
2. Map source-specific schemas into UTC intervals without resolving DST ambiguity by guesswork.
3. Validate uniqueness, interval completeness, units, signs, nulls and revision identifiers.
4. Diagnose the target before modeling: zeros, skew, monthly/hourly patterns, autocorrelation,
   regional distribution, event count and run duration.
5. Construct D-1 features and mask every observation published after issuance.
6. Use chronological expanding-window validation; preprocessing is learned inside each fold.
7. Compare operational baselines with logistic, random forest, LightGBM and XGBoost classifiers.
8. If zero inflation warrants it, fit event classification plus positive-volume regressors and
   P10/P50/P90 quantiles. Report calibration and PR-AUC prominently.
9. Compare nested models with/without price and cross-border features to test incremental predictive
   information. Claims remain associational.
10. Produce T-24h/T+24h event studies, global/local SHAP views, seasonal metrics and drift checks.
11. Run price-only, forecast-aware and perfect-information battery schedules under identical physical
   constraints. Sweep probability thresholds and false-negative costs.

Random splits are forbidden. Final test data are touched once. Model artifacts record configuration,
feature list, package versions, training window and data checksum.

