import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np


st.set_page_config(
    page_title="Annual Salary Prediction for AI Job",
    page_icon="💼",
    layout="wide"
)

df = pd.read_csv("ai_job_dataset.csv")

# Convert user-friendly labels back to original dataset values for encoding
company_size = company_size.replace({"Small": "S", "Medium": "M", "Large": "L"})
employment_type = employment_type.replace({"Full Time": "FT", "Part Time": "PT", "Contract": "CT", "Freelance": "FL"})
experience_level = experience_level.replace({"Entry Level": "EN", "Mid Level": "MI", "Senior Level": "SE", "Executive": "EX"})

# ==================== PAGE INTRO ==================== #
st.title("💼 AI/ML Annual Salary Prediction Dashboard")

st.write("""
Welcome to the **AI/ML Salary Prediction System**!  
This dashboard uses a **CatBoost Machine Learning model** trained on real job market data  
to **predict annual salaries** based on job role, experience, and company profile.

📌 Use this tool to:
- Estimate salaries for different AI/ML job positions
- Compare salary expectations globally
- Gain insights into career growth and market demand
""")

st.info("💡 *All salary values are predicted in USD and converted into MYR for convenience.*")

st.divider()

# ==================== INPUT SECTION ==================== #
st.subheader("🔍 Enter Job & Company Details")
st.write("Provide information below to generate a salary estimation based on similar roles in the industry.")

# Replace raw labels with user-friendly text
df_display = df.copy()
df_display["company_size"] = df_display["company_size"].replace({
    "S": "Small",
    "M": "Medium",
    "L": "Large"
})

df_display["employment_type"] = df_display["employment_type"].replace({
    "FT": "Full Time",
    "PT": "Part Time",
    "CT": "Contract",
    "FL": "Freelance"
})

df_display["experience_level"] = df_display["experience_level"].replace({
    "EN": "Entry Level",
    "MI": "Mid Level",
    "SE": "Senior Level",
    "EX": "Executive"
})

# Organize selectors into columns
col1, col2, col3 = st.columns(3)

with col1:
    job_title = st.selectbox("Job Title", ["None"] + sorted(df_display["job_title"].unique().tolist()))
    employment_type = st.selectbox("Employment Type", ["None"] + sorted(df_display["employment_type"].unique().tolist()))

with col2:
    experience_level = st.selectbox("Experience Level", ["None"] + sorted(df_display["experience_level"].unique().tolist()))
    company_location = st.selectbox("Company Location", ["None"] + sorted(df_display["company_location"].unique().tolist()))

with col3:
    company_size = st.selectbox("Company Size", ["None"] + sorted(df_display["company_size"].unique().tolist()))
    education_required = st.selectbox("Education Required", ["None"] + sorted(df_display["education_required"].unique().tolist()))

# Years of experience full width
years_experience = st.slider("Years of Experience", min_value=0, max_value=30, value=3)

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
        if input_data[col].dtype == "object":
            if col in label_encoders:
                le = label_encoders[col]
                input_data[col] = input_data[col].apply(lambda x: x if x in le.classes_ else le.classes_[0])
                input_data[col] = le.transform(input_data[col])
            else:
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

        prediction_log = model.predict(input_encoded)[0]
        salary_pred_usd = float(np.expm1(prediction_log))

        st.success(f"💰 Predicted Annual Salary: **${salary_pred_usd:,.2f} USD**")

        salary_myr = salary_pred_usd * 4.7
        st.info(f"🇲🇾 Equivalent Salary: **RM{salary_myr:,.2f} MYR**")

    except Exception as e:
        st.error(f"⚠️ Error occurred while predicting: {e}")

# ==================== EXPLANATION / PERFORMANCE ==================== #
st.divider()
st.subheader("📈 Model Performance & Information")

st.write("""
This prediction is powered by a **CatBoost Regressor**, optimized for handling categorical job attributes.

### ✅ Model Evaluation Results (Log-Scale)
- **MSE (log):** 0.019985  
- **RMSE (log):** 0.141369  
- **R² Score (log):** 0.918697  

🧠 *The model explains over 91% of the variance in salaries — indicating strong prediction capability.*
""")

st.caption("📊 Model trained using real-world AI job dataset. Powered by Machine Learning ⚙️")
