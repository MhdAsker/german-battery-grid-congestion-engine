from __future__ import annotations


def explain_model(model, X, *, max_background: int = 500):
    """Return SHAP values. Interpret as predictive association, never causation."""
    try:
        import shap
    except ImportError as exc:
        raise ImportError("Install project with the 'ml' extra to use SHAP") from exc
    background = X.sample(min(len(X), max_background), random_state=42)
    explainer = shap.Explainer(model, background)
    return explainer(X)

