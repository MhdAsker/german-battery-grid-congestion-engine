from gridflex.forecasting.metrics import classification_metrics, quantile_metrics


def test_metrics_have_imbalance_relevant_scores():
    result = classification_metrics([0, 0, 1, 1], [0.1, 0.2, 0.7, 0.9])
    assert {"pr_auc", "brier", "roc_auc", "precision", "recall"} <= result.keys()


def test_interval_coverage():
    result = quantile_metrics([1, 2], {0.1: [0, 1], 0.5: [1, 2], 0.9: [2, 3]})
    assert result["p10_p90_coverage"] == 1

