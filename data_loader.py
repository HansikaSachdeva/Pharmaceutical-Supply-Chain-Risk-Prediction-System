import pandas as pd
from joblib import load
import os

def load_data():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    df = pd.read_csv(os.path.join(base_dir, "data", "final_dataset.csv"))
    df['initial_posting_date'] = pd.to_datetime(
        df['initial_posting_date'],
        errors='coerce'
    )
    return df

def load_model():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return load(os.path.join(base_dir, "model", "model.joblib"))