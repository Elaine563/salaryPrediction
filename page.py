import streamlit as st
import pandas as pd
import numpy as np
import joblib
from catboost import CatBoostRegressor

# Load model and encoders
model = joblib.load("salary_predictor.pkl")
label_encoders = joblib.load("label_encoders.pkl")

st.set_page_config(page_title="AI/ML Salary Predictor", page_icon="💰", layout="centered")

st.title("💼 AI/ML Salary Prediction App")
st.markdown("Predict your estimated salary (in USD) based on job and personal details.")

# Load dataset to populate dropdowns
df = pd.read_csv("ai_job_dataset.csv")

# --- USER INPUTS ---

# Optional dropdowns for categorical features
job_title = st.selectbox("Job Title (optional):", [""] + sorted(df["job_title"].dropna().unique().tolist()))
experience_level = st.selectbox("Experience Level:", ["EN", "MI", "SE", "EX"])
employment_type = st.selectbox("Employment Type:", ["FT", "PT", "CT", "FL"])
company_location = st.selectbox("Company Location (optional):", [""] + sorted(df["company_location"].dropna().unique().tolist()))
company_size = st.selectbox("Company Size:", ["S", "M", "L"])
education_required = st.selectbox("Education Required:", ["Associate", "Bachelor", "Master", "PhD"])

# Slider for numerical input
years_experience = st.slider("Years of Experience:", min_value=0.0, max_value=50.0, step=0.5)

# --- PREPARE INPUT ---
input_data = pd.DataFrame({
    'job_title': [job_title if job_title else "Unknown"],
    'experience_level': [experience_level],
    'employment_type': [employment_type],
    'company_location': [company_location if company_location else "Unknown"],
    'company_size': [company_size],
    'education_required': [education_required],
    'years_experience': [years_experience]
})

# Encode categorical columns
for col, le in label_encoders.items():
    if col in input_data.columns:
        # Handle unseen values safely
        input_data[col] = input_data[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        input_data[col] = le.transform(input_data[col])

# --- PREDICT SALARY ---
if st.button("💡 Predict Salary"):
    try:
        prediction_log = model.predict(input_data)[0]  # model predicts log(salary)
        prediction_usd = np.expm1(prediction_log)      # convert back to normal scale

        st.success(f"💵 Estimated Salary: **${prediction_usd:,.2f} USD**")

        with st.expander("🔍 Encoded Input Data"):
            st.dataframe(input_data)

    except Exception as e:
        st.error(f"⚠️ An error occurred while making the prediction.\n\n**Error details:** {str(e)}")
