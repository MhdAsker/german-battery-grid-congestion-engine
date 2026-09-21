from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    average_precision_score, brier_score_loss, f1_score, mean_absolute_error,
    mean_pinball_loss, mean_squared_error, precision_score, recall_score, roc_auc_score,
)


def classification_metrics(y_true, probability, threshold: float = 0.5) -> dict[str, float]:
    prediction = np.asarray(probability) >= threshold
    y = np.asarray(y_true)
    result = {
        "precision": precision_score(y, prediction, zero_division=0),
        "recall": recall_score(y, prediction, zero_division=0),
        "f1": f1_score(y, prediction, zero_division=0),
        "pr_auc": average_precision_score(y, probability),
        "brier": brier_score_loss(y, probability),
    }
    result["roc_auc"] = roc_auc_score(y, probability) if len(np.unique(y)) == 2 else np.nan
    return result


def quantile_metrics(y_true, predictions: dict[float, np.ndarray]) -> dict[str, float]:
    result = {f"pinball_p{int(q*100)}": mean_pinball_loss(y_true, pred, alpha=q)
              for q, pred in predictions.items()}
    median = predictions[0.5]
    result["mae_p50"] = mean_absolute_error(y_true, median)
    result["rmse_p50"] = mean_squared_error(y_true, median) ** 0.5
    if 0.1 in predictions and 0.9 in predictions:
        y = np.asarray(y_true)
        result["p10_p90_coverage"] = np.mean((y >= predictions[0.1]) & (y <= predictions[0.9]))
    return result

