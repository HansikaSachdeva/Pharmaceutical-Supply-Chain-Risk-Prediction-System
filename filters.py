import streamlit as st
import pandas as pd

# ----------------------------------
# Sidebar Styling
# ----------------------------------
def apply_sidebar_style():
    st.markdown("""
    <style>

    section[data-testid="stSidebar"] {
        background-color: #1e293b;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] label {
        color: white !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #1e293b !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] input {
        background-color: #1e293b !important;
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)


# ----------------------------------
# Filters
# ----------------------------------
def apply_filters(df):

    # Apply sidebar styling
    apply_sidebar_style()

    st.sidebar.header("Filters")

    # Threshold
    risk_threshold = st.sidebar.slider("Risk Threshold", 0.0, 1.0, 0.3)

    # Dropdown filters
    manufacturers = st.sidebar.multiselect(
        "Manufacturer",
        sorted(df['company_name'].dropna().unique())
    )

    categories = st.sidebar.multiselect(
        "Therapeutic Category",
        sorted(df['therapeutic_category'].dropna().unique())
    )

    dosage_forms = st.sidebar.multiselect(
        "Dosage Form",
        sorted(df['dosage_form'].dropna().unique())
    )

    risk_levels = st.sidebar.multiselect(
        "Risk Level",
        ["High", "Medium", "Low"]
    )

    # Date range
    min_date = df['initial_posting_date'].min()
    max_date = df['initial_posting_date'].max()

    date_range = st.sidebar.date_input(
        "Date Range",
        [min_date, max_date]
    )

    # Apply filters
    filtered_df = df.copy()

    filtered_df = filtered_df[filtered_df['risk_score'] >= risk_threshold]

    if manufacturers:
        filtered_df = filtered_df[filtered_df['company_name'].isin(manufacturers)]

    if categories:
        filtered_df = filtered_df[filtered_df['therapeutic_category'].isin(categories)]

    if dosage_forms:
        filtered_df = filtered_df[filtered_df['dosage_form'].isin(dosage_forms)]

    if risk_levels:
        filtered_df = filtered_df[filtered_df['risk_level'].isin(risk_levels)]

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df['initial_posting_date'] >= pd.to_datetime(date_range[0])) &
            (filtered_df['initial_posting_date'] <= pd.to_datetime(date_range[1]))
        ]

    return filtered_df