import numpy as np

FEATURES = [
    'log_manufacturer_count','log_days_since_last_shortage',
    'complexity_Low','complexity_Medium',
    'manufacturer_risk','category_demand_score',
    'reason_manufacturing','reason_demand',
    'is_injectable','is_tablet','is_capsule',
    'manufacturer_risk_scaled'
]

def add_features(df, model):
    
    df['risk_score'] = model.predict_proba(df[FEATURES])[:, 1]

    df = df.groupby('generic_name').agg({
        'risk_score': 'max',
        'manufacturer_risk': 'mean',
        'category_demand_score': 'mean',
        'company_name': 'first',
        'therapeutic_category': 'first',
        'dosage_form': 'first',
        'initial_posting_date': 'first'
    }).reset_index()

    df['risk_percentile'] = df['risk_score'].rank(pct=True)

    q1 = df['risk_score'].quantile(0.33)
    q2 = df['risk_score'].quantile(0.66)

    def risk_bucket(x):
        if x >= q2: return "High"
        elif x >= q1: return "Medium"
        else: return "Low"

    df['risk_level'] = df['risk_score'].apply(risk_bucket)

    df['critical_flag'] = (
        (df['manufacturer_risk'] > 0.5) &
        (df['category_demand_score'] > 0.5)
    )

    def get_action(row):
        if row['critical_flag']:
            return "Immediate sourcing + stockpile"
        elif row['risk_level'] == "High":
            return "Increase inventory + monitor suppliers"
        elif row['risk_level'] == "Medium":
            return "Monitor demand trends"
        else:
            return "No action"

    df['recommended_action'] = df.apply(get_action, axis=1)

    return df