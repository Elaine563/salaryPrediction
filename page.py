import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and encoders
model = joblib.load("salary_predictor.pkl")
label_encoders = joblib.load("label_encoders.pkl")

st.title("💰 AI/ML Job Salary Prediction App")
st.write("Fill in the details below to predict your expected salary (in USD).")

# Load dataset to get column structure if needed
df = pd.read_csv("ai_job_dataset.csv")

# --- USER INPUTS ---

# Categorical (optional dropdowns)
job_title = st.selectbox("Job Title (optional):", 
                         options=[""] + sorted(df["job_title"].dropna().unique().tolist()))

experience_level = st.selectbox("Experience Level:", 
                                options=["EN", "MI", "SE", "EX"])

employment_type = st.selectbox("Employment Type:", 
                               options=["FT", "PT", "CT", "FL"])

company_location = st.selectbox("Company Location (optional):", 
                                options=[""] + sorted(df["company_location"].dropna().unique().tolist()))

company_size = st.selectbox("Company Size:", 
                            options=["S", "M", "L"])

education_required = st.selectbox("Education Required:", 
                                  options=["Associate", "Bachelor", "Master", "PhD"])

# Numeric slider
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

# Encode categorical columns using stored encoders
for col, le in label_encoders.items():
    if col in input_data.columns:
        # Handle unseen categories gracefully
        input_data[col] = input_data[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        input_data[col] = le.transform(input_data[col])

# --- PREDICT ---
if st.button("Predict Salary"):
    prediction_log = model.predict(input_data)[0]  # model trained on log
    prediction_usd = np.expm1(prediction_log)      # convert back to normal scale

    st.success(f"💵 Estimated Salary: **${prediction_usd:,.2f} USD**")

    with st.expander("🔍 Encoded Input Data"):
        st.dataframe(input_data)
