import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np


st.set_page_config(
    page_title="AI/ML Salary Prediction",
    page_icon="💼",
    layout="wide"
)

df = pd.read_csv("ai_job_dataset.csv")
try:
    with open("salary_predictor.pkl", "rb") as f:
        model = pickle.load(f)
    st.sidebar.success("✅ Model Loaded Successfully")
except Exception as e:
    st.sidebar.error(f"❌ Error loading model: {e}")
    st.stop()

try:
    with open("label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)
    st.sidebar.success("✅ Label Encoders Loaded")
except Exception as e:
    st.sidebar.warning("⚠️ No label encoders found. Using new encoding.")
    label_encoders = {}

# ==================== PAGE INTRO ==================== #
st.title("💼 AI/ML Salary Prediction System")
st.write("""
This app predicts **AI/ML professional salaries** using a trained **CatBoost Regressor model**.
Select job details below to get an estimated salary.
""")

st.divider()

# ==================== INPUT SECTION ==================== #
st.subheader("🔍 Enter Job & Company Details")

job_title = st.selectbox("Job Title", sorted(df["job_title"].unique()))
experience_level = st.selectbox("Experience Level", sorted(df["experience_level"].unique()))
employment_type = st.selectbox("Employment Type", sorted(df["employment_type"].unique()))
company_location = st.selectbox("Company Location", sorted(df["company_location"].unique()))
company_size = st.selectbox("Company Size", sorted(df["company_size"].unique()))
education_required = st.selectbox("Education Required", sorted(df["education_required"].unique()))
years_experience = st.slider("Years of Experience", min_value=0, max_value=30, value=5)

st.divider()

# ==================== ENCODING FUNCTION ==================== #
def encode_input(job_title, experience_level, employment_type,
                 company_location, company_size,
                 education_required, years_experience):

    input_data = pd.DataFrame({
        "job_title": [job_title],
        "experience_level": [experience_level],
        "employment_type": [employment_type],
        "company_location": [company_location],
        "company_size": [company_size],
        "education_required": [education_required],
        "years_experience": [years_experience]
    })

    for col in input_data.columns:
        if col in label_encoders:
            le = label_encoders[col]
            input_data[col] = le.transform(input_data[col])
        elif input_data[col].dtype == "object":
            le = LabelEncoder()
            input_data[col] = le.fit_transform(input_data[col])

    return input_data

# ==================== PREDICTION SECTION ==================== #
if st.button("🚀 Predict Salary"):
    try:
        input_encoded = encode_input(
            job_title, experience_level, employment_type,
            company_location, company_size, education_required, years_experience
        )

        prediction_log = model.predict(input_encoded)[0]  # Model trained on log(salary)
        salary_pred_usd = np.exp(prediction_log)  # Reverse log transformation

        st.success(f"💰 Predicted Salary: **${salary_pred_usd:,.2f} USD**")

        salary_myr = salary_pred_usd * 4.7
        st.info(f"🇲🇾 Equivalent Salary: **RM{salary_myr:,.2f} MYR**")

    except Exception as e:
        st.error(f"⚠️ Error occurred while predicting: {e}")

# ==================== FOOTER ==================== #
st.divider()
st.caption("📊 Model trained on AI Job Dataset — Powered by CatBoost Regressor.")
