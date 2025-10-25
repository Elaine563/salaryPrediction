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

col1, col2 = st.columns([3, 1])  # Adjust ratio as needed

with col2:
    st.image("ai.png", use_container_width=True)


df = pd.read_csv("ai_job_dataset.csv")  # original dataset

# ==================== INTRO ==================== #
st.title("💼 AI/ML Annual Salary Prediction Dashboard")

st.write("""
Welcome to the **Annual Salary Prediction Dashboard**!  
This dashboard uses a **CatBoost Machine Learning model** trained on real job market data  
to **predict annual salaries** based on job role, experience, and company profile.

📌 Use this tool to:
- Estimate salaries for different AI/ML job positions
- Compare salary expectations globally
- Gain insights into career growth and market demand
""")

st.info("💡 *All salary values are predicted in USD and converted into MYR for convenience.*")

st.divider()

# ==================== INPUTS ==================== #
st.subheader("🔍 Job & Company Details")
st.write("Provide information below to generate a salary estimation based on similar roles in the industry.")

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

# ✅ Layout using columns
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

years_experience = st.slider("Years of Experience", 0, 30, 3)

st.divider()

# ==================== ENCODING ==================== #
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

# ==================== PREDICT ==================== #
if st.button("🚀 Predict Salary"):

    if job_title == "None":
        st.warning("⚠️ Please select at least Job Title.")
    else:
        try:
            # ✅ Convert user-friendly labels back before encoding
            company_size = company_size.replace({"Small": "S", "Medium": "M", "Large": "L"})
            employment_type = employment_type.replace({"Full Time": "FT", "Part Time": "PT", "Contract": "CT", "Freelance": "FL"})
            experience_level = experience_level.replace({"Entry Level": "EN", "Mid Level": "MI", "Senior Level": "SE", "Executive": "EX"})

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
            st.error(f"⚠️ Prediction failed: {e}")

# ==================== PERFORMANCE ==================== #
st.divider()
st.subheader("📈 Model Performance")

st.write("""
This prediction model is powered by **CatBoost Regressor**,  
which handles categorical job attributes efficiently and provides high-accuracy results.

### ✅ Performance Metrics (Log-Scaled)
- **MSE:** 0.019985  
- **RMSE:** 0.141369  
- **R² Score:** 0.918697  

🧠 *The model captures over 91% of salary variance — strong predictive accuracy!*
""")

st.caption("📊 Data-driven insights powered by Machine Learning — CatBoost Model ⚙️")
st.caption("Predictions are estimates based on historical data trends and may vary depending on real-world conditions.")
