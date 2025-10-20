import streamlit as st
import pandas as pd
import numpy as np
import joblib

# --- LOAD MODEL & ENCODERS ---
@st.cache_resource
def load_assets():
    model = joblib.load("salary_predictor.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    df = pd.read_csv("ai_job_dataset.csv")
    return model, label_encoders, df

model, label_encoders, df = load_assets()

# --- APP TITLE ---
st.title("💰 AI/ML Job Salary Prediction App")
st.write("Predict your estimated **AI/ML job salary (in USD)** based on your experience, education, and company details.")

# --- USER INPUTS ---
job_title = st.selectbox("Job Title (optional):", 
                         options=[""] + sorted(df["job_title"].dropna().unique().tolist()))
experience_level = st.selectbox("Experience Level:", ["EN", "MI", "SE", "EX"])
employment_type = st.selectbox("Employment Type:", ["FT", "PT", "CT", "FL"])
company_location = st.selectbox("Company Location (optional):", 
                                options=[""] + sorted(df["company_location"].dropna().unique().tolist()))
company_size = st.selectbox("Company Size:", ["S", "M", "L"])
education_required = st.selectbox("Education Required:", ["Associate", "Bachelor", "Master", "PhD"])
years_experience = st.slider("Years of Experience:", min_value=0.0, max_value=50.0, step=0.5)

# --- PREPARE INPUT DATA ---
input_data = pd.DataFrame({
    'job_title': [job_title if job_title else "Unknown"],
    'experience_level': [experience_level],
    'employment_type': [employment_type],
    'company_location': [company_location if company_location else "Unknown"],
    'company_size': [company_size],
    'education_required': [education_required],
    'years_experience': [years_experience]
})

# --- ENCODE CATEGORICAL COLUMNS ---
for col, le in label_encoders.items():
    if col in input_data.columns:
        input_data[col] = input_data[col].astype(str)  # ensure string type
        input_data[col] = input_data[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
        input_data[col] = le.transform(input_data[col])

# --- PREDICT SALARY ---
if st.button("💵 Predict Salary"):
    try:
        prediction_log = model.predict(input_data)[0]  # model predicts log salary
        prediction_usd = np.expm1(prediction_log)      # convert back to normal scale
        st.success(f"💰 **Estimated Salary:** ${prediction_usd:,.2f} USD")

        with st.expander("🔍 Encoded Input Data"):
            st.dataframe(input_data)

    except Exception as e:
        st.error("⚠️ An error occurred while making the prediction.")
        st.write("Error details:", str(e))
