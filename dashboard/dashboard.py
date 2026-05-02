import streamlit as st
from data_loader import load_data, load_model
from feature_engineering import add_features
from filters import apply_filters
from kpi import show_kpis
from charts import show_charts

st.set_page_config(layout="wide")

st.title("Drug Shortage Risk Dashboard")
st.markdown("### Proactive Monitoring of Pharmaceutical Supply Chain Risk")
st.caption("Identify high-risk drugs, understand supply vulnerabilities, and take early action to prevent shortages.")

# Load
df = load_data()
model = load_model()

# Features
df = add_features(df, model)

# Filters
filtered_df = apply_filters(df)

# KPIs
show_kpis(filtered_df)

# Charts
show_charts(filtered_df)
