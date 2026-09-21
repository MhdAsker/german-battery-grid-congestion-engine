from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from gridflex.battery import optimize_dispatch
from gridflex.config import BatteryConfig, load_config
from gridflex.event_study import event_windows
from gridflex.features.targets import target_diagnostics

st.set_page_config(page_title="German GridFlex", layout="wide")
PAGES = ["Germany System Overview", "Curtailment Monitor", "24h Forecast",
         "Model Explainability", "Historical Event Explorer", "Storage Opportunity Simulator"]
page = st.sidebar.radio("Page", PAGES)
data_path = Path(st.sidebar.text_input("Validated dataset", "data/processed/unified.parquet"))
st.title(page)

if not data_path.exists():
    st.info("No validated dataset found. Run ingestion and validation first; the dashboard will not fabricate demo data.")
    st.stop()

df = pd.read_parquet(data_path).sort_index()
if df.index.tz is None:
    st.error("Dataset index must be timezone-aware UTC.")
    st.stop()

if page == "Germany System Overview":
    columns = [c for c in ["load_forecast_mw", "wind_forecast_mw", "solar_forecast_mw"] if c in df]
    st.plotly_chart(px.line(df.reset_index(), x=df.index.name, y=columns), use_container_width=True)
elif page == "Curtailment Monitor":
    threshold = st.number_input("Event threshold (MWh)", min_value=0.0, value=0.1)
    st.json(target_diagnostics(df.curtailment_mwh, threshold))
    st.plotly_chart(px.area(df.reset_index(), x=df.index.name, y="curtailment_mwh"), use_container_width=True)
elif page == "24h Forecast":
    required = ["event_probability", "p10_mwh", "p50_mwh", "p90_mwh"]
    missing = set(required) - set(df)
    if missing:
        st.warning(f"Forecast artifact columns missing: {sorted(missing)}")
    else:
        date = st.date_input("Delivery date", value=df.index[-1].date())
        selected = df[df.index.tz_convert("Europe/Berlin").date == date]
        st.plotly_chart(px.line(selected.reset_index(), x=df.index.name, y=required), use_container_width=True)
elif page == "Model Explainability":
    shap_file = Path("reports/shap_values.parquet")
    if not shap_file.exists():
        st.info("Run the trained-model SHAP export first. Explanations will not be inferred from placeholders.")
    else:
        values = pd.read_parquet(shap_file).abs().mean().sort_values(ascending=False)
        st.plotly_chart(px.bar(values, orientation="h", title="Mean absolute SHAP value"), use_container_width=True)
        st.caption("SHAP values describe predictive association, not causation.")
elif page == "Historical Event Explorer":
    windows = event_windows(df)
    if not windows:
        st.info("No events at the configured threshold.")
    else:
        event = st.selectbox("Event start (UTC)", list(windows))
        st.plotly_chart(px.line(windows[event].reset_index(), x=df.index.name,
                                y=[c for c in ["wind_forecast_mw", "solar_forecast_mw",
                                  "load_forecast_mw", "curtailment_mwh"] if c in df]), use_container_width=True)
else:
    config = load_config()["battery"]
    power = st.number_input("Power (MW)", min_value=0.1, value=float(config["power_mw"]))
    energy = st.number_input("Energy (MWh)", min_value=0.1, value=float(config["energy_mwh"]))
    config.update(power_mw=power, energy_mwh=energy, maximum_soc_mwh=energy,
                  initial_soc_mwh=min(config["initial_soc_mwh"], energy))
    if "day_ahead_price_eur_mwh" not in df:
        st.warning("Day-ahead price column required.")
    else:
        horizon = df.tail(96)
        result = optimize_dispatch(horizon.day_ahead_price_eur_mwh, BatteryConfig(**config),
            opportunity_mwh=horizon.get("p50_mwh"),
            opportunity_probability=horizon.get("event_probability"))
        st.metric("Counterfactual objective", f"€{result.objective_eur:,.0f}")
        st.plotly_chart(px.line(result.schedule.reset_index(), x=df.index.name,
                                y=["charge_mw", "discharge_mw", "soc_mwh"]), use_container_width=True)
        st.caption("System-level scenario only; it does not establish asset eligibility or revenue.")

