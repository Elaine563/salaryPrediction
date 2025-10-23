import streamlit as st
import pandas as pd
import pickle
import numpy as np
from catboost import CatBoostRegressor

st.set_page_config(page_title="AI/ML Salary Prediction", layout="wide")

# Load model
try:
    with open("salary_predictor.pkl", "rb") as f:
        model = pickle.load(f)
except Exception as e:
    st.error(f"❌ Failed to load model: {e}")
    st.stop()

# Load label encoders if you have them
try:
    with open("label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
except:
    label_encoders = {}

st.title("💼 AI/ML Salary Prediction")

# Input form
with st.form("prediction_form"):
    st.subheader("Enter Employee Information")

    country = st.selectbox("Country", ["United States", "India", "Germany", "Malaysia"])
    experience = st.slider("Years of Experience", 0, 20, 3)
    education = st.selectbox("Education Level", ["Bachelor's", "Master's", "PhD"])
    job_title = st.selectbox("Job Title", ["Data Scientist", "ML Engineer", "AI Researcher", "Software Engineer"])
    company_size = st.selectbox("Company Size", ["Small", "Medium", "Large"])

    submitted = st.form_submit_button("Predict Salary")

if submitted:
    try:
        # Encode categorical columns
        input_dict = {
            "Country": country,
            "Experience": experience,
            "Education": education,
            "Job Title": job_title,
            "Company Size": company_size
        }

        input_df = pd.DataFrame([input_dict])

        for col in label_encoders:
            if col in input_df.columns:
                input_df[col] = label_encoders[col].transform(input_df[col])

        # Predict
        prediction = model.predict(input_df)[0]
        st.success(f"💰 Predicted Salary: ${prediction:,.2f}")

    except Exception as e:
        st.error(f"⚠️ An error occurred while making the prediction.\n\nError details: {e}")
