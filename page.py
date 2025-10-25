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

df = pd.read_csv("ai_job_dataset.csv")  # original dataset

# ✅ Load trained model + encoders
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

# ==================== INTRO ==================== #
st.title("💼 AI/ML Annual Salary Prediction Dashboard")

st.write("""
This dashboard predicts **annual salaries for AI & ML professionals** using real-world job
market data and a **CatBoost Regressor model** trained for high prediction accuracy.

📌 Explore and compare expected salaries across:
- Job positions
- Experience levels
- Employment types
- Company sizes and locations
""")

st.info("💡 Salary estimates are shown in both USD and MYR 🇲🇾")

st.divider()

# ==================== INPUTS ==================== #
st.subheader("🔍 Job & Company Details")

# ✅ Friendly text replacements for UI selections
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
