import streamlit as st

def show_kpis(df):

    col1, col2, col3, col4, col5 = st.columns(5)

    def kpi(label, value):
        st.markdown(f"""
        <div style="
            padding:18px;
            border-radius:12px;
            background-color:#1e293b;
            text-align:center;
        ">
            <div style="font-size:13px;color:white;">{label}</div>
            <div style="font-size:26px;font-weight:bold;color:white;">{value}</div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        kpi("Total Drugs", len(df))

    with col2:
        kpi("Avg Risk", round(df['risk_score'].mean(), 2))

    with col3:
        kpi("Median Risk", round(df['risk_score'].median(), 2))

    with col4:
        kpi("Manufacturers", df['company_name'].nunique())

    with col5:
        kpi("Critical Drugs", df['critical_flag'].sum())
