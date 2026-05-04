# Pharmaceutical Supply Chain Risk Prediction System

This project develops an end-to-end **supply chain risk prediction system** that forecasts drug shortages using FDA data and translates model outputs into **actionable decisions** through an interactive dashboard.

<img width="1920" height="1080" alt="Screenshot 2026-05-03 164952" src="https://github.com/user-attachments/assets/4ac0e380-721b-48b5-9e53-a449e3c12716" />

## Capabilities

- Predict probability of future drug shortages  
- Identify high-risk drugs and prioritize interventions  
- Analyze supply-side vulnerabilities (manufacturer concentration)  
- Provide actionable recommendations for supply chain decisions  
- Deliver explainable insights using rule-based and AI-assisted explanations  

## Dataset

Two FDA datasets combined:

### 1. Drug Shortage Data
- Source: FDA Drug Shortage Database  
- Contains shortage events, reasons, and timelines  
- Used to define the **target variable (future shortage)**  

### 2. Orange Book Data
- Source: FDA Orange Book  
- Contains manufacturer and product-level information  
- Used to construct **supply-side features**  

## Methodology

### Data Integration
- Standardized drug identifiers for both datasets  
- Merged shortage data with supply-side features (~18% unmatched records)  


### Feature Engineering

The model incorporates both **supply-side and demand-side signals**:

- **Manufacturer Risk** → historical supplier instability  
- **Manufacturer Count** → supply diversification  
- **Days Since Last Shortage** → temporal recency  
- **Category Demand Score** → demand pressure proxy  
- **Shortage Reasons** → operational signals  
- **Dosage Form Indicators** → complexity proxy  


### Target Variable

- **future_shortage**
  - 1 → drug experiences a shortage in the next observed event  
  - 0 → no subsequent shortage  


### Modeling

Models evaluated:
- Logistic Regression  
- Random Forest  
- Gradient Boosting  
- XGBoost  

**Final Model: Gradient Boosting**

Selection based on:
- Balanced precision-recall tradeoff  
- Strong overall performance  
- Robust handling of non-linear relationships  

## Model Performance

- ROC-AUC ≈ 0.80  
- High recall prioritized to minimize missed shortages  
- Interpretable feature importance highlighting key risk drivers  


## Key Insights

- **Supplier instability is the strongest predictor of shortages**  
- **Demand pressure significantly contributes to risk**  
- **Recent shortages strongly indicate future disruptions**  
- Even drugs with multiple manufacturers can experience systemic shortages  

## Dashboard (Decision System)

The Streamlit dashboard transforms model outputs into **actionable insights**:

### Features

- **Risk Distribution & Trends** → portfolio-level monitoring  
- **Decision Matrix** → risk vs volume analysis  
- **Supplier Concentration Analysis** → dependency insights  
- **Drug Decision Panel**:
  - WHY the drug is at risk  
  - WHAT is driving the risk  
  - WHAT action to take  

## Explainability Layer

- Rule-based explanations derived from feature values  
- Optional AI-assisted explanations (LLM) for business-friendly insights

## Business Applications

This system enables:

- **Pharmaceutical Companies**
  - Production planning and risk mitigation  

- **Hospitals & Distributors**
  - Inventory optimization and shortage preparedness  

- **Regulators**
  - Monitoring systemic supply chain risks

## Project Structure
pharma-supply-chain-risk/
│
├── data/
│ └── final_dataset.csv
│ └── manufacturer_counts.csv
│ └── products.csv
│ └── shortage_data.csv
│ └── drug-shortages.json
│
├── model/
│ └── model.joblib
│
├── notebooks/
│ ├── 1.fda_drug_shortages.ipynb
│ ├── 2.fda_orange_book
│ ├── 3.merged.ipynb
│
├── dashboard/
│ ├── dashboard.py
│ ├── charts.py
│ ├── filters.py
│ ├── feature_engineering.py
│ ├── data_loader.py
│ ├── ai_explainer.py
│
├── README.md
