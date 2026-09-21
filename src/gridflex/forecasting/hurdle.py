from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from sklearn.base import clone
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression


@dataclass
class HurdleForecaster:
    classifier: object = field(default_factory=lambda: LogisticRegression(max_iter=2000, class_weight="balanced"))
    quantiles: tuple[float, ...] = (0.1, 0.5, 0.9)

    def fit(self, X, y_event, y_volume):
        self.classifier_ = clone(self.classifier).fit(X, y_event)
        mask = np.asarray(y_event).astype(bool)
        if mask.sum() < 10:
            raise ValueError("At least 10 event observations are required for conditional volume models")
        self.volume_models_ = {}
        for q in self.quantiles:
            model = HistGradientBoostingRegressor(loss="quantile", quantile=q, random_state=42)
            self.volume_models_[q] = model.fit(X.loc[mask], np.asarray(y_volume)[mask])
        return self

    def predict(self, X) -> dict[str, object]:
        probability = self.classifier_.predict_proba(X)[:, 1]
        conditional = {q: np.maximum(0, model.predict(X)) for q, model in self.volume_models_.items()}
        unconditional = {q: probability * value for q, value in conditional.items()}
        return {"event_probability": probability, "conditional_volume": conditional,
                "expected_volume": unconditional}

