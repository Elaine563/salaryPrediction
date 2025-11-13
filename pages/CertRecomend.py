import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import plotly.express as px
import plotly.graph_objects as go

# -------------------- LOAD DATASET --------------------
df = pd.read_csv("ai_job_dataset.csv")  # adjust path

# Standardize column names: lowercase & strip spaces
df.columns = df.columns.str.lower().str.strip()

st.title("AI Career Learning Path")

# -------------------- TOP BANNER --------------------
st.image(
    "images/upskill.PNG",  
    use_container_width=True  # spans the full width of the page/container
)


# -------------------- USER SELECTION --------------------
job_titles = df['job_title'].unique()
selected_job = st.selectbox("Select a Job Title", job_titles)

# Filter dataset for the selected job
job_data = df[df['job_title'] == selected_job]

# -------------------- SKILLS PROCESSING --------------------
if 'required_skills' in df.columns:
    skills_series = job_data['required_skills'].dropna().str.split(',').explode().str.strip()
    skills_count = skills_series.value_counts()
else:
    st.error("⚠️ 'required_skills' column not found in dataset.")
    skills_count = pd.Series([])

# -------------------- DATA VISUALIZATION --------------------
st.subheader("Top Skills Required")
if not skills_count.empty:
    top_skills = skills_count.head(10)
    
    # Prepare dot plot (lollipop chart) data
    dot_df = pd.DataFrame({
        'Skill': top_skills.index,
        'Count': top_skills.values
    })
    
    fig = go.Figure()
    
    # Add stems (lines)
    for i, row in dot_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Skill'], row['Skill']],
            y=[0, row['Count']],
            mode='lines',
            line=dict(color='lightgray', width=2),
            showlegend=False
        ))
    
    # Add dots
    fig.add_trace(go.Scatter(
        x=dot_df['Skill'],
        y=dot_df['Count'],
        mode='markers+text',
        marker=dict(size=15, color=px.colors.qualitative.Set2),
        text=dot_df['Count'],
        textposition='top center',
        name='Count'
    ))
    
    fig.update_layout(
        title="Top 10 Skills for Selected Job",
        xaxis_title="Skill",
        yaxis_title="Count",
        paper_bgcolor='rgba(245,245,245,1)',
        font=dict(size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No skill data available for this job.")

# -------------------- SKILL → CERTIFICATION MAPPING --------------------
usd_to_myr = 4.8
skill_to_cert = {
    "Python": [
        {"name": "Python for Everybody (Coursera)", "duration": "4 weeks", "fee_usd": 49, "link": "https://www.coursera.org/specializations/python"},
        {"name": "AWS Machine Learning Specialty", "duration": "6 weeks", "fee_usd": 300, "link": "https://aws.amazon.com/certification/certified-machine-learning-specialty/"}
    ],
    "Machine Learning": [
        {"name": "Machine Learning by Andrew Ng", "duration": "11 weeks", "fee_usd": 0, "link": "https://www.coursera.org/learn/machine-learning"},
        {"name": "TensorFlow Developer Certificate", "duration": "8 weeks", "fee_usd": 100, "link": "https://www.tensorflow.org/certificate"}
    ],
    "NLP": [
        {"name": "Natural Language Processing with Deep Learning (Coursera)", "duration": "6 weeks", "fee_usd": 79, "link": "https://www.coursera.org/learn/natural-language-processing"}
    ],
    "Data Analysis": [
        {"name": "Data Analyst Nanodegree (Udacity)", "duration": "12 weeks", "fee_usd": 399, "link": "https://www.udacity.com/course/data-analyst-nanodegree--nd002"},
        {"name": "Google Data Analytics Certificate", "duration": "6 months", "fee_usd": 0, "link": "https://grow.google/certificates/data-analytics/"}
    ],
    "Deep Learning": [
        {"name": "Deep Learning Specialization (Coursera)", "duration": "12 weeks", "fee_usd": 49, "link": "https://www.coursera.org/specializations/deep-learning"}
    ]
}

st.subheader("Select Skills You Already Know")
known_skills = st.multiselect("Tick the skills you already know:", skills_count.index.tolist() if not skills_count.empty else [])

# -------------------- RECOMMEND CERTIFICATIONS --------------------
recommended = []

for skill in skills_count.index if not skills_count.empty else []:
    if skill not in known_skills and skill in skill_to_cert:
        for course in skill_to_cert[skill]:
            fee_myr = course["fee_usd"] * usd_to_myr
            fee_display = "Free" if fee_myr == 0 else f"RM {fee_myr:,.0f}"
            recommended.append((skill, f"{course['name']} - {course['duration']} - {fee_display}", course["link"]))

if recommended:
    rec_df = pd.DataFrame(recommended, columns=["Skill", "Course & Duration & Fee", "Link"])
    
    # Create a 3-column markdown table
    markdown_table = "| Skill | Course & Duration & Fee | Link |\n|---|---|---|\n"
    for i, row in rec_df.iterrows():
        markdown_table += f"| {row['Skill']} | {row['Course & Duration & Fee']} | [Go to Course]({row['Link']}) |\n"
    
    st.markdown("### Recommended Certifications / Courses")
    st.markdown(markdown_table, unsafe_allow_html=True)
else:
    st.info("🎉 You already know all top skills! No additional certifications recommended.")

# -------------------- AVERAGE SALARY INFO --------------------
if 'salary_usd' in job_data.columns and not job_data['salary_usd'].empty:
    avg_salary = job_data['salary_usd'].mean()
    avg_salary_myr = avg_salary * usd_to_myr
    st.markdown(f"**Average Salary for {selected_job}:** USD ${avg_salary:,.0f} | RM {avg_salary_myr:,.0f}")
else:
    st.info("Salary information not available for this job.")

# -------------------- DOWNLOAD PDF --------------------
def generate_pdf(df, job_title):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Learning Path for {job_title}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    for i, row in df.iterrows():
        pdf.multi_cell(0, 8, f"Skill: {row['Skill']}\nCourse: {row['Course & Duration & Fee']}\nLink: {row['Link']}")
        pdf.ln(5)

    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

if recommended:
    pdf_bytes = generate_pdf(rec_df, selected_job)
    st.download_button(
        label="📄 Download Learning Path as PDF",
        data=pdf_bytes,
        file_name=f"{selected_job}_Learning_Path.pdf",
        mime="application/pdf"
    )
