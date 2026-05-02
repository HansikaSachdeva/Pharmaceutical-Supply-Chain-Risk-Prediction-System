import streamlit as st
import pandas as pd
from streamlit_echarts import st_echarts

def section_gap():
    st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)


def show_charts(df):

    section_gap()
    col1, col2, col3 = st.columns(3)

    # ----------------------------
    # Risk Distribution
    # ----------------------------
    order = ["Low", "Medium", "High"]
    risk_counts = df['risk_level'].value_counts().reindex(["Low","Medium","High"]).fillna(0)

    color_map = {
    "High": "#1e293b",   
    "Medium": "#475569", 
    "Low": "#94a3b8"     
    }

    data = []

    for level in order:
        value = int(risk_counts.get(level, 0))

        data.append({
            "value": value,
            "itemStyle": {
                "color": color_map[level],   
                "borderRadius": [6, 6, 0, 0]
            }
        })

    option = {
    "title": {
        "text": "Risk Distribution",
        "subtext": "Current portfolio exposure across low, medium, and high shortage risk drugs",
        "left": "center",
        "textStyle": {
            "fontSize": 16,
            "fontWeight": "bold"
        },
        "subtextStyle": {
            "fontSize": 12,
            "color": "#6b7280"
        }
    },

    "grid": {
        "top": 80,   
        "left": 60,
        "right": 20,
        "bottom": 50
    },

    "xAxis": {
        "type": "category",
        "name": "Risk Level",
        "nameLocation": "middle",
        "nameGap": 30,
        "data": risk_counts.index.tolist()
    },

    "yAxis": {
        "type": "value",
        "name": "Number of Drugs",
        "nameLocation": "middle",
        "nameGap": 40
    },

    "series": [{
        "data": data,
        "type": "bar",
        "label": {
            "show": True,
            "position": "top"
        }
    }]
    }
    with col1:
        st_echarts(option, height="300px")

    # ----------------------------
    # Decision Matrix
    # ----------------------------
    cat = (
        df.groupby('therapeutic_category')
        .agg(avg_risk=('risk_score','mean'), count=('generic_name','count'))
        .reset_index()
    )

    data = [[row['count'], row['avg_risk']] for _, row in cat.iterrows()]

    option = {
    "title": {
        "text": "Risk vs Volume Decision Matrix",
        "subtext": "Identifies high-impact therapeutic areas combining shortage risk and supply volume",
        "left": "center",
        "textStyle": {
            "fontSize": 16,
            "fontWeight": "bold"
        },
        "subtextStyle": {
            "fontSize": 12,
            "color": "#6b7280"
        }
    },

    "grid": {
        "top": 80,  
        "left": 60,
        "right": 20,
        "bottom": 50
    },

    "xAxis": {
        "name": "Volume (# Drugs)",
        "type": "value",
        "nameLocation": "middle"
    },

    "yAxis": {
        "name": "Average Risk",
        "type": "value",
        "nameLocation": "middle",
        "min": 0,
        "max": 1
    },

    "series": [{
        "type": "scatter",
        "data": data,
        "symbolSize": 20,

        "itemStyle": {
            "color": """
            function(params){
                if(params.data[1] > 0.7) return '#1e293b';   // high risk
                if(params.data[1] > 0.4) return '#475569';   // medium
                return '#94a3b8';                            // low
            }
            """
        }
    }],

    "markLine": {
        "silent": True,
        "lineStyle": {
            "type": "dashed",
            "color": "#999"
        },
        
    }
    }

    with col2:
        st_echarts(option, height="300px")

    # ----------------------------
    # Supplier Concentration
    # ----------------------------
    top_manu = df['company_name'].value_counts().head(7)

    option = {
    "title": {
        "text": "Supplier Concentration ",
        "subtext": "Highlights dependency on key manufacturers and potential supply concentration risks",
        "left": "center"
    },

    "xAxis": {
        "type": "value",
        "name": "Number of Drugs",
        "nameLocation": "middle"
    },
    "yAxis": {
        "type": "category",
        "data": top_manu.index.tolist(),
        "axisLabel": {
            "interval": 0,   
            "width": 150,    
            "overflow": "truncate"  
        }
    },

    "series": [{
        "data": top_manu.values.tolist(),
        "type": "bar",
        "itemStyle": {
            "color": "#1e293b",
            "borderRadius": [0, 6, 6, 0]
        },
        "label": {
            "show": True,
            "position": "right"
        }
    }]
    }
    with col3:
        st_echarts(option, height="350px")

    # ----------------------------
    # Row 2
    # ----------------------------
    col1, col2 = st.columns(2)

    # Supply Risk Matrix
    scatter_data = df[['manufacturer_risk','category_demand_score']].dropna()

    option = {
    "title": {
        "text": "Supply Risk Matrix",
        "subtext": "Maps demand pressure against supplier reliability to pinpoint vulnerable supply nodes",
        "left": "center"
    },

    "grid": {
        "top": 80,
        "left": 60,
        "right": 20,
        "bottom": 50
    },

    "xAxis": {
        "type": "value",
        "name": "Manufacturer Risk",
        "nameLocation": "middle",
        "min": 0,
        "max": 1
    },

    "yAxis": {
        "type": "value",
        "name": "Demand Pressure",
        "nameLocation": "middle",
        "min": 0,
        "max": 1
    },

    "series": [{
        "type": "scatter",
        "data": scatter_data.values.tolist(),
        "symbolSize": 10,

        "itemStyle": {
            "color": "#1e293b"
        },

        "markLine": {
            "silent": True,
            "lineStyle": {"type": "dashed", "color": "#999"},
            "data": [
                {"xAxis": 0.5},
                {"yAxis": 0.5}
            ]
        }
    }]
    }
    with col1:
        st_echarts(option, height="300px")

    # Trend
    trend = df.copy()
    trend['month'] = trend['initial_posting_date'].dt.to_period('M').astype(str)
    trend = trend.groupby('month')['risk_score'].mean().reset_index()

    option = {
    "title": {
        "text": "Risk Trend Over Time",
        "subtext": "Tracks how shortage risk is evolving to detect emerging supply disruptions early",
        "left": "center"
    },

    "grid": {
        "top": 80,
        "left": 60,
        "right": 20,
        "bottom": 50
    },

    
    "xAxis": {
        "type": "category",
        "data": trend['month'].tolist(),
        "axisLabel": {
            "rotate": 30   
        }
    },
    "yAxis": {
        "type": "value",
        "name": "Avg Risk",
        "nameLocation": "middle"
    },
    "series": [{
        "data": trend['risk_score'].tolist(),
        "type": "line",
        "smooth": True,   
        "symbol": "circle",
        "symbolSize": 6,
        "lineStyle": {
            "color": "#1e293b",
            "width": 3
        },
        "itemStyle": {
            "color": "#1e293b"
        },
        "areaStyle": {   
            "color": "rgba(30,41,59,0.1)"
        }
    }],
    "tooltip": {
        "trigger": "axis"
    }
    }
    with col2:
        st_echarts(option, height="300px")

    # ----------------------------
    # Priority Table
    # ----------------------------
    col1,col2 = st.columns(2)

    with col1:
        st.markdown("### Priority Drug List")

        st.dataframe(
            df.sort_values(by='risk_score', ascending=False)[
                ['generic_name','risk_level','recommended_action']
            ].head(20),
            height=280,
            use_container_width=True
        )
    
    with col2:
        st.markdown("### Drug Insight")

        if len(df) > 0:

            drug = st.selectbox(
                "Select Drug",
                df['generic_name'].unique(),
                key="drug_selector_main"
            )

            row = df[df['generic_name'] == drug].iloc[0]

            #explanation
            def explain_risk(row):
                reasons = []
                if row.get('manufacturer_risk', 0) > 0.4:
                    reasons.append("high manufacturer risk")
                if row.get('category_demand_score', 0) > 0.3:
                    reasons.append("high demand pressure")
                return ", ".join(reasons) if reasons else "moderate combined risk"

            explanation_text = explain_risk(row)

            #color
            if row['risk_level'] == "High":
                bg_color = "#F9A6A6"

            elif row['risk_level'] == "Medium":
                bg_color = "#FDFBD5"

            else:
                bg_color = "#C2EBBC"

            #card = html
            st.markdown(f"""
            <div style="
                background-color:{bg_color};
                padding:16px;
                border-radius:12px;
                margin-top:10px;
            ">
                <div style="margin-top:10px;"><b>Risk Score: </b>{round(row['risk_score'],3)}</div>
                <div style="margin-top:10px;"><b>Risk Level: </b>{row['risk_level']}</div>
                <div style="margin-top:10px;"><b>Drivers: </b>{explanation_text}</div>
                <div style="margin:10px 0px;"><b>Recommended Action: </b>{row['recommended_action']}</div>
            </div>
            """, unsafe_allow_html=True)