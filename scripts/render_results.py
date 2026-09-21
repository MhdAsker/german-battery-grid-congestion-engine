"""Render README result charts from measured backtest artifacts.

This command intentionally fails when result files are absent or incomplete. It never creates
synthetic metrics. Expected inputs live under reports/results/ and are produced by the research run.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


REQUIRED = {
    "classification_metrics.csv": {"model", "split", "pr_auc", "brier"},
    "calibration.csv": {"model", "mean_probability", "event_rate", "count"},
    "quantile_metrics.csv": {"model", "quantile", "pinball_loss"},
    "battery_value.csv": {"strategy", "objective_eur"},
}


def read_checked(root: Path, name: str) -> pd.DataFrame:
    path = root / name
    if not path.exists():
        raise FileNotFoundError(f"Missing measured result artifact: {path}")
    frame = pd.read_csv(path)
    missing = REQUIRED[name] - set(frame.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")
    if frame.empty:
        raise ValueError(f"{path} contains no measured results")
    return frame


def save(fig: go.Figure, output: Path, name: str) -> None:
    fig.update_layout(template="plotly_white", font_family="Arial", margin=dict(l=60, r=25, t=70, b=55))
    fig.write_image(output / name, width=1100, height=620)


def render(result_dir: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    scores = read_checked(result_dir, "classification_metrics.csv")
    held_out = scores[scores["split"].eq("test")]
    if held_out.empty:
        raise ValueError("classification_metrics.csv must contain held-out rows with split='test'")
    long = held_out.melt(id_vars="model", value_vars=["pr_auc", "brier"],
                         var_name="metric", value_name="score")
    save(px.bar(long, x="model", y="score", color="metric", barmode="group",
                title="Held-out event-forecast performance"), output_dir, "model_comparison.svg")

    calibration = read_checked(result_dir, "calibration.csv")
    fig = px.line(calibration, x="mean_probability", y="event_rate", color="model", markers=True,
                  title="Probability calibration on held-out predictions")
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Perfect calibration",
                             line=dict(dash="dash", color="#777")))
    save(fig, output_dir, "calibration.svg")

    quantiles = read_checked(result_dir, "quantile_metrics.csv")
    save(px.bar(quantiles, x="quantile", y="pinball_loss", color="model", barmode="group",
                title="Conditional-volume quantile loss"), output_dir, "quantile_loss.svg")

    battery = read_checked(result_dir, "battery_value.csv")
    save(px.bar(battery, x="strategy", y="objective_eur", color="strategy",
                title="Counterfactual battery objective by information strategy"),
         output_dir, "battery_value.svg")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=Path("reports/results"))
    parser.add_argument("--output", type=Path, default=Path("reports/figures"))
    arguments = parser.parse_args()
    render(arguments.results, arguments.output)
