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

job_title = st.selectbox("Job Title", ["None"] + sorted(df["job_title"].unique().tolist()))
experience_level = st.selectbox("Experience Level", ["None"] + sorted(df["experience_level"].unique().tolist()))
employment_type = st.selectbox("Employment Type", ["None"] + sorted(df["employment_type"].unique().tolist()))
company_location = st.selectbox("Company Location", ["None"] + sorted(df["company_location"].unique().tolist()))
company_size = st.selectbox("Company Size", ["None"] + sorted(df["company_size"].unique().tolist()))
education_required = st.selectbox("Education Required", ["None"] + sorted(df["education_required"].unique().tolist()))
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
