import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib
import os
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from fpdf import FPDF

st.set_page_config(
       page_title="💰 Annual Salary Prediction for AI Job",
    page_icon="🌍",
    layout="wide"
)

df = pd.read_csv("ai_job_dataset.csv")  
df.columns = df.columns.str.lower().str.strip()

# ==================== CONSTANTS FOR NEW FEATURES ==================== #
USD_TO_MYR = 4.13

SKILL_CERTIFICATIONS = {
    "Python": [
        {"name": "Python for Everybody (Coursera)", "duration": "4 weeks", "fee_usd": 49, 
         "link": "https://www.coursera.org/specializations/python", "impact": "Foundation", "salary_boost": 5000},
        {"name": "AWS Machine Learning Specialty", "duration": "6 weeks", "fee_usd": 300, 
         "link": "https://aws.amazon.com/certification/certified-machine-learning-specialty/", "impact": "High", "salary_boost": 15000}
    ],
    "Machine Learning": [
        {"name": "Machine Learning by Andrew Ng", "duration": "11 weeks", "fee_usd": 0, 
         "link": "https://www.coursera.org/learn/machine-learning", "impact": "High", "salary_boost": 20000},
        {"name": "TensorFlow Developer Certificate", "duration": "8 weeks", "fee_usd": 100, 
         "link": "https://www.tensorflow.org/certificate", "impact": "Medium", "salary_boost": 12000}
    ],
    "NLP": [
        {"name": "Natural Language Processing Specialization", "duration": "6 weeks", "fee_usd": 79, 
         "link": "https://www.coursera.org/specializations/natural-language-processing", "impact": "High", "salary_boost": 18000}
    ],
    "Deep Learning": [
        {"name": "Deep Learning Specialization (Coursera)", "duration": "12 weeks", "fee_usd": 49, 
         "link": "https://www.coursera.org/specializations/deep-learning", "impact": "High", "salary_boost": 22000}
    ],
    "Data Analysis": [
        {"name": "Google Data Analytics Certificate", "duration": "6 months", "fee_usd": 0, 
         "link": "https://grow.google/certificates/data-analytics/", "impact": "Foundation", "salary_boost": 8000}
    ],
    "AWS": [
        {"name": "AWS Certified Solutions Architect", "duration": "8 weeks", "fee_usd": 150, 
         "link": "https://aws.amazon.com/certification/", "impact": "High", "salary_boost": 16000}
    ],
    "Docker": [
        {"name": "Docker Mastery (Udemy)", "duration": "4 weeks", "fee_usd": 15, 
         "link": "https://www.udemy.com/course/docker-mastery/", "impact": "Medium", "salary_boost": 8000}
    ],
    "Kubernetes": [
        {"name": "Certified Kubernetes Administrator (CKA)", "duration": "6 weeks", "fee_usd": 395, 
         "link": "https://www.cncf.io/certification/cka/", "impact": "High", "salary_boost": 17000}
    ],
    "SQL": [
        {"name": "SQL for Data Science (Coursera)", "duration": "4 weeks", "fee_usd": 49, 
         "link": "https://www.coursera.org/learn/sql-for-data-science", "impact": "Foundation", "salary_boost": 6000}
    ],
    "Tableau": [
        {"name": "Tableau Desktop Specialist Certification", "duration": "3 weeks", "fee_usd": 100, 
         "link": "https://www.tableau.com/learn/certification", "impact": "Medium", "salary_boost": 9000}
    ],
    "PyTorch": [
        {"name": "PyTorch for Deep Learning (Udacity)", "duration": "8 weeks", "fee_usd": 0, 
         "link": "https://www.udacity.com/course/deep-learning-pytorch--ud188", "impact": "High", "salary_boost": 15000}
    ],
    "Linux": [
        {"name": "Linux Foundation Certified System Administrator", "duration": "6 weeks", "fee_usd": 300, 
         "link": "https://training.linuxfoundation.org/certification/", "impact": "Medium", "salary_boost": 10000}
    ],
    "Hadoop": [
        {"name": "Cloudera Certified Data Engineer", "duration": "10 weeks", "fee_usd": 400, 
         "link": "https://www.cloudera.com/about/training/certification.html", "impact": "High", "salary_boost": 18000}
    ],
    "Scala": [
        {"name": "Scala Programming Specialization", "duration": "7 weeks", "fee_usd": 79, 
         "link": "https://www.coursera.org/specializations/scala", "impact": "Medium", "salary_boost": 12000}
    ],
    "Java": [
        {"name": "Oracle Certified Java Programmer", "duration": "8 weeks", "fee_usd": 245, 
         "link": "https://education.oracle.com/java-se-11-developer", "impact": "Medium", "salary_boost": 11000}
    ],
    "Mathematics": [
        {"name": "Mathematics for Machine Learning Specialization", "duration": "10 weeks", "fee_usd": 49, 
         "link": "https://www.coursera.org/specializations/mathematics-machine-learning", "impact": "Foundation", "salary_boost": 7000}
    ]
}

# ==================== ORIGINAL SALARY PREDICTION CODE (UNTOUCHED) ==================== #
header_col1, header_col2 = st.columns([3, 1.2]) 

with header_col1:
    st.title("🌍 AI/ML Annual Salary Prediction Dashboard")
    st.write("""
Welcome to the **Annual Salary Prediction Dashboard**!  
This dashboard uses a **CatBoost Machine Learning model** trained on real job market data  
to **predict annual salaries** based on job role, experience, and company profile.

Use this tool to:
- Estimate salaries for different AI/ML job positions
- Compare salary expectations globally
- Gain insights into career growth and market demand
""")

with header_col2:
    st.image("ai.png", width=350) 
    
st.info("💡 *All salary values are predicted in USD and converted into MYR for convenience.*")

st.divider()

# ==================== INPUT SECTION ==================== #
st.subheader("🔍 Job & Company Details")
st.write("Provide information below to generate a salary estimation based on similar roles in the industry.")

df_display = df.copy()
df_display["company_size"] = df_display["company_size"].replace({"S": "Small", "M": "Medium", "L": "Large"})
df_display["employment_type"] = df_display["employment_type"].replace({"FT": "Full Time", "PT": "Part Time", "CT": "Contract", "FL": "Freelance"})
df_display["experience_level"] = df_display["experience_level"].replace({"EN": "Entry Level", "MI": "Mid Level", "SE": "Senior Level", "EX": "Executive"})

# ✅ Column layout
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

# ==================== MODEL LOAD ==================== #
BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "salary_predictor.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "label_encoders.pkl")

try:
    # load model
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    # load encoders (use joblib if saved with joblib)
    label_encoders = joblib.load(ENCODER_PATH)

except Exception as e:
    st.error(f"❌ Model or Label Encoder missing!\nCheck files in folder {BASE_DIR}\nError: {e}")
    st.stop()

# ==================== PREDICTION ==================== #
if st.button("Predict Salary"):

    if job_title == "None":
        st.warning("⚠️ Please select at least Job Title.")
    else:
        try:
            # ✅ Convert UI labels → dataset labels using pandas Series replace()
            company_size_converted = pd.Series([company_size]).replace({"Small": "S", "Medium": "M", "Large": "L"}).iloc[0]
            employment_type_converted = pd.Series([employment_type]).replace({"Full Time": "FT", "Part Time": "PT", "Contract": "CT", "Freelance": "FL"}).iloc[0]
            experience_level_converted = pd.Series([experience_level]).replace({"Entry Level": "EN", "Mid Level": "MI", "Senior Level": "SE", "Executive": "EX"}).iloc[0]

            input_encoded = encode_input(
                job_title, experience_level_converted, employment_type_converted,
                company_location, company_size_converted, education_required, years_experience
            )

            # ✅ Predict (log scale → convert back)
            prediction_log = model.predict(input_encoded)[0]
            salary_pred_usd = float(np.expm1(prediction_log))

            # ✅ Display results
            st.success(f"Predicted Annual Salary: **${salary_pred_usd:,.2f} USD**")
            salary_myr = salary_pred_usd * 4.7
            st.info(f"🇲🇾 Equivalent Salary: **RM{salary_myr:,.2f} MYR**")
            
            # Store in session state for new features
            st.session_state['predicted_salary'] = salary_pred_usd
            st.session_state['job_title'] = job_title
            st.session_state['experience_level'] = experience_level_converted
            st.session_state['employment_type'] = employment_type_converted
            st.session_state['company_location'] = company_location
            st.session_state['company_size'] = company_size_converted
            st.session_state['education_required'] = education_required
            st.session_state['years_experience'] = years_experience

        except Exception as e:
            st.error(f"⚠️ Prediction failed: {e}")

# ==================== MODEL PERFORMANCE ==================== #
st.divider()
st.subheader("Model Performance")

st.write("""
This prediction model is powered by **CatBoost Regressor**,  
which handles categorical job attributes efficiently and provides high-accuracy results.

### Performance Metrics (Log Scale)
- **MSE:** 0.019985  
- **RMSE:** 0.141369  
- **R² Score:** 0.918697  

*The model captures over 91% of salary variance — strong predictive accuracy!*
""")

st.caption("Data-driven insights powered by Machine Learning — CatBoost Model ⚙️")
st.caption("Predictions are estimates based on historical trends and may vary based on real-world conditions.")

# ==================== NEW FEATURES BELOW (AFTER PREDICTION) ==================== #

if 'predicted_salary' in st.session_state:
    st.markdown("---")
    st.markdown("## What's Next? Your Career Growth Path")
    
    predicted_salary = st.session_state['predicted_salary']
    job_title_selected = st.session_state['job_title']
    
    # ==================== SECTION 1: MARKET COMPARISON ==================== #
    st.subheader("How Does Your Salary Compare to the Market?")
    
    job_market_data = df[df['job_title'] == job_title_selected]['salary_usd'].dropna()
    
    if not job_market_data.empty:
        avg_market = job_market_data.mean()
        min_market = job_market_data.min()
        max_market = job_market_data.max()
        percentile = (job_market_data < predicted_salary).sum() / len(job_market_data) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Your Monthly Salary", f"RM {(predicted_salary * USD_TO_MYR / 12):,.0f}")
        with col2:
            diff = predicted_salary - avg_market
            st.metric("vs Market Avg", f"RM {(avg_market * USD_TO_MYR / 12):,.0f}", f"RM {(diff * USD_TO_MYR / 12):+,.0f}")
        with col3:
            st.metric("Market Range", f"RM {(min_market * USD_TO_MYR / 12):,.0f} - RM {(max_market * USD_TO_MYR / 12):,.0f}")
        with col4:
            st.metric("Your Percentile", f"{percentile:.0f}th", 
                     "Above Avg" if percentile > 50 else "Below Avg")
        
        # Salary distribution visualization
        fig_dist = go.Figure()
        
        # Convert salaries to MYR monthly for display
        job_market_data_myr = (job_market_data * USD_TO_MYR) / 12
        predicted_salary_myr = (predicted_salary * USD_TO_MYR) / 12
        
        fig_dist.add_trace(go.Histogram(
            x=job_market_data_myr,
            name='Market Salaries',
            marker_color='lightblue',
            opacity=0.7,
            nbinsx=20
        ))
        fig_dist.add_vline(
            x=predicted_salary_myr, 
            line_dash="dash", 
            line_color="red",
            line_width=3,
            annotation_text=f"Your Salary: RM {predicted_salary_myr:,.0f}",
            annotation_position="top"
        )
        fig_dist.update_layout(
            title=f"Salary Distribution for {job_title_selected}",
            xaxis_title="Monthly Salary (MYR)",
            yaxis_title="Number of Jobs",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    st.divider()
    
    # ==================== SECTION 2: SKILLS GAP & CERTIFICATIONS ==================== #
    st.subheader("Boost Your Salary with Certifications")
    st.write("Based on your job role, here are skills that can increase your earning potential:")
    
    # Get required skills for the job
    job_skills_data = df[df['job_title'] == job_title_selected]
    
    if 'required_skills' in df.columns and not job_skills_data.empty:
        skills_series = job_skills_data['required_skills'].dropna().str.split(',').explode().str.strip()
        skills_count = skills_series.value_counts().head(10)
        
        # Let user select known skills
        st.markdown("#### Select Skills You Already Have:")
        known_skills = st.multiselect(
            "Check the skills you're proficient in:",
            skills_count.index.tolist(),
            key="known_skills_cert"
        )
        
        # Identify missing skills
        missing_skills = [skill for skill in skills_count.index if skill not in known_skills]
        
        if missing_skills:
            st.markdown(f"#### Skills to Develop ({len(missing_skills)} identified):")
            
            # Build recommendation list
            recommendations = []
            for skill in missing_skills:
                if skill in SKILL_CERTIFICATIONS:
                    for course in SKILL_CERTIFICATIONS[skill]:
                        roi_value = course["salary_boost"] / course["fee_usd"] if course["fee_usd"] > 0 else 999999
                        recommendations.append({
                            "Skill": skill,
                            "Course": course["name"],
                            "Duration": course["duration"],
                            "Fee (USD)": course["fee_usd"],
                            "Fee (MYR)": course["fee_usd"] * USD_TO_MYR,
                            "Impact": course["impact"],
                            "Salary Boost": course["salary_boost"],
                            "ROI": roi_value,
                            "Link": course["link"]
                        })
            
            if recommendations:
                rec_df = pd.DataFrame(recommendations)
                rec_df = rec_df.sort_values("ROI", ascending=False)
                
                # ROI Bubble Chart
                fig_roi = px.scatter(
                    rec_df,
                    x="Fee (MYR)",
                    y="Salary Boost",
                    size="ROI",
                    color="Impact",
                    hover_data=["Course", "Skill", "Duration"],
                    color_discrete_map={"Foundation": "#3498db", "Medium": "#f39c12", "High": "#e74c3c"},
                    title="Certification ROI Analysis: Cost vs Salary Impact",
                    labels={"Fee (MYR)": "Course Fee (MYR)", "Salary Boost": "Monthly Salary Increase (MYR)"}
                )
                fig_roi.update_layout(height=500)
                st.plotly_chart(fig_roi, use_container_width=True)
                
                # Investment Summary
                total_investment = rec_df['Fee (USD)'].sum()
                total_boost = rec_df['Salary Boost'].sum()
                new_potential_salary = predicted_salary + total_boost
                
                st.markdown("### Investment Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Investment", f"RM {total_investment * USD_TO_MYR:,.0f}")
                with col2:
                    st.metric("Monthly Increase", f"+RM {(total_boost * USD_TO_MYR / 12):,.0f}", f"+{(total_boost/predicted_salary*100):.1f}%")
                with col3:
                    st.metric("New Monthly Target", f"RM {(new_potential_salary * USD_TO_MYR / 12):,.0f}")
                with col4:
                    overall_roi = total_boost / total_investment if total_investment > 0 else 999999
                    roi_display = f"{overall_roi:.1f}x" if overall_roi < 999999 else "Unlimited"
                    st.metric("Overall ROI", roi_display)
                
                # Detailed Course Table
                st.markdown("### Recommended Courses (Sorted by ROI)")
                
                for idx, row in rec_df.head(10).iterrows():
                    impact_icon = 'High' if row['Impact'] == 'High' else 'Medium' if row['Impact'] == 'Medium' else 'Foundation'
                    with st.expander(f"[{impact_icon}] **{row['Skill']}** - {row['Course']}"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.markdown(f"**Duration:** {row['Duration']}")
                        with col2:
                            fee_text = 'Free' if row['Fee (USD)'] == 0 else f"RM {row['Fee (MYR)']:.0f}"
                            st.markdown(f"**Fee:** {fee_text}")
                        with col3:
                            st.markdown(f"**Salary Boost:** +RM {(row['Salary Boost'] * USD_TO_MYR / 12):,.0f}/month")
                        with col4:
                            roi_text = f"{row['ROI']:.1f}x" if row['ROI'] < 999999 else "Unlimited"
                            st.markdown(f"**ROI:** {roi_text}")
                        
                        st.markdown(f"**[Enroll Now]({row['Link']})**")
                
                # PDF Download
                def generate_career_pdf(rec_df, job_title, current_salary, potential_salary):
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", 'B', 18)
                    pdf.cell(0, 10, "Career Growth Plan", ln=True, align='C')
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", '', 12)
                    pdf.cell(0, 8, f"Job Title: {job_title}", ln=True)
                    pdf.cell(0, 8, f"Current Monthly Salary: RM {(current_salary * USD_TO_MYR / 12):,.0f}", ln=True)
                    pdf.cell(0, 8, f"Potential Monthly Salary: RM {(potential_salary * USD_TO_MYR / 12):,.0f}", ln=True)
                    increase_pct = ((potential_salary - current_salary) / current_salary * 100)
                    pdf.cell(0, 8, f"Potential Monthly Increase: RM {((potential_salary - current_salary) * USD_TO_MYR / 12):,.0f} ({increase_pct:.1f}%)", ln=True)
                    pdf.ln(10)
                    
                    pdf.set_font("Arial", 'B', 14)
                    pdf.cell(0, 10, "Recommended Certifications", ln=True)
                    pdf.ln(5)
                    
                    pdf.set_font("Arial", '', 10)
                    for _, row in rec_df.iterrows():
                        pdf.multi_cell(0, 6, 
                            f"Skill: {row['Skill']}\n" +
                            f"Course: {row['Course']}\n" +
                            f"Duration: {row['Duration']} | Fee: RM {row['Fee (USD)'] * USD_TO_MYR:.0f} | Impact: {row['Impact']}\n" +
                            f"Monthly Salary Boost: +RM {(row['Salary Boost'] * USD_TO_MYR / 12):,.0f}\n" +
                            f"Link: {row['Link']}\n")
                        pdf.ln(3)
                    
                    pdf_bytes = BytesIO()
                    pdf.output(pdf_bytes)
                    pdf_bytes.seek(0)
                    return pdf_bytes
                
                pdf_data = generate_career_pdf(rec_df, job_title_selected, predicted_salary, new_potential_salary)
                st.download_button(
                    label="Download Complete Career Plan (PDF)",
                    data=pdf_data,
                    file_name=f"Career_Plan_{job_title_selected}.pdf",
                    mime="application/pdf"
                )
            else:
                st.info("Certifications for these skills are being updated. Check back soon!")
        else:
            st.success("Amazing! You have all the top skills for this role!")
    
    st.divider()
    
# ==================== SECTION 3: REALISTIC NEXT STEP COMPANIES ==================== #
    st.subheader("Target Companies for Your Next Career Move (Monthly Salary)")
    st.write(f"Companies offering salaries **5-30% higher** than your predicted salary for **{job_title_selected}** - realistic next steps:")
    
    # Get companies with salaries close to but higher than prediction
    if 'company_name' in df.columns:
        job_companies = df[df['job_title'] == job_title_selected][['company_name', 'salary_usd', 'company_location', 'company_size']].dropna()
        
        if not job_companies.empty:
            # Filter companies with salary 5-30% higher than predicted
            lower_bound = predicted_salary * 1.05  # 5% higher
            upper_bound = predicted_salary * 1.30  # 30% higher
            
            realistic_companies = job_companies[
                (job_companies['salary_usd'] >= lower_bound) & 
                (job_companies['salary_usd'] <= upper_bound)
            ]
            
            # If not enough companies in range, expand the range
            if len(realistic_companies) < 5:
                lower_bound = predicted_salary * 1.00  # Same level
                upper_bound = predicted_salary * 1.50  # Up to 50% higher
                realistic_companies = job_companies[
                    (job_companies['salary_usd'] >= lower_bound) & 
                    (job_companies['salary_usd'] <= upper_bound)
                ]
            
            # Get top 10 from this filtered set
            top_companies = realistic_companies.nlargest(10, 'salary_usd')
            
            if not top_companies.empty:
                # Convert to MYR monthly for display
                top_companies_display = top_companies.copy()
                top_companies_display['monthly_salary_myr'] = (top_companies_display['salary_usd'] * USD_TO_MYR) / 12
                top_companies_display['increase_pct'] = ((top_companies_display['salary_usd'] - predicted_salary) / predicted_salary * 100)
                
                # Show salary range info
                st.info(f"Your Current Prediction: **RM {(predicted_salary * USD_TO_MYR / 12):,.0f}/month** | Showing companies offering **RM {(lower_bound * USD_TO_MYR / 12):,.0f} - RM {(upper_bound * USD_TO_MYR / 12):,.0f}/month**")
                
                # Bar chart of target companies
                fig_companies = px.bar(
                    top_companies_display,
                    x='monthly_salary_myr',
                    y='company_name',
                    orientation='h',
                    color='increase_pct',
                    hover_data=['company_location', 'increase_pct'],
                    title=f"Realistic Target Companies for {job_title_selected} (Monthly Salary)",
                    labels={'monthly_salary_myr': 'Monthly Salary (MYR)', 'company_name': 'Company', 'increase_pct': 'Increase %'},
                    color_continuous_scale='Greens'
                )
                fig_companies.update_layout(height=500, showlegend=True)
                st.plotly_chart(fig_companies, use_container_width=True)
                
                # Table view
                st.markdown("### Detailed Company Information")
                display_companies = top_companies_display.copy()
                display_companies['salary_display'] = display_companies['monthly_salary_myr'].apply(lambda x: f"RM {x:,.0f}")
                display_companies['increase_display'] = display_companies['increase_pct'].apply(lambda x: f"+{x:.1f}%")
                display_companies['company_size'] = display_companies['company_size'].replace({'S': 'Small', 'M': 'Medium', 'L': 'Large'})
                display_companies = display_companies[['company_name', 'salary_display', 'increase_display', 'company_location', 'company_size']]
                display_companies = display_companies.rename(columns={
                    'company_name': 'Company',
                    'salary_display': 'Monthly Salary (MYR)',
                    'increase_display': 'Salary Increase',
                    'company_location': 'Location',
                    'company_size': 'Size'
                })
                st.dataframe(display_companies, use_container_width=True, hide_index=True)
            else:
                st.warning("No companies found in the realistic salary range. Consider upskilling to reach higher salary brackets!")
        else:
            st.info("No company data available for this role.")
    else:
        st.info("Company information not available in dataset.")
    
    st.markdown("---")
    st.success("Next Steps: Choose certifications, target top companies, and plan your career progression!")