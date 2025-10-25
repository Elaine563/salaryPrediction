import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Insights", page_icon="📈", layout="wide")

# ---------------- Load Data ---------------- #
df = pd.read_csv("ai_job_dataset.csv")

# ---------------- Sidebar Filters ---------------- #
st.sidebar.header("Filters")
job_options = ["All"] + sorted(df["job_title"].unique())
selected_job = st.sidebar.selectbox("Select Job Title:", job_options)

df_filtered = df if selected_job == "All" else df[df["job_title"] == selected_job]

# ---------------- KPIs ---------------- #
st.markdown("## 📊 Job Market Insights Dashboard")
st.markdown(f"### Showing insights for: **{selected_job}**")

avg_salary = df_filtered["salary_usd"].mean() if len(df_filtered) > 0 else 0
total_jobs = len(df_filtered)
top_location = df_filtered["employee_residence"].mode()[0] if len(df_filtered) > 0 else "N/A"

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Average Salary (USD)", f"${avg_salary:,.0f}")
kpi2.metric("Total Jobs", total_jobs)
kpi3.metric("Top Location", top_location)

st.divider()

# ---------------- Salary Choropleth Map ---------------- #
st.subheader("🌍 Global Salary by Country")
salary_data = df_filtered.groupby("employee_residence")["salary_usd"].mean().reset_index()

map_fig = px.choropleth(
    salary_data,
    locations="employee_residence",
    locationmode="country names",
    color="salary_usd",
    color_continuous_scale=px.colors.sequential.Bluered,
    hover_name="employee_residence",
    hover_data={"salary_usd":":,.0f"},
    title="Average Salary (USD)",
)

map_fig.update_layout(
    title_x=0.5,
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth",
        bgcolor="rgba(0,0,0,0)"
    ),
    margin=dict(l=0, r=0, t=50, b=0),
    coloraxis_colorbar=dict(title="USD")
)

st.plotly_chart(map_fig, use_container_width=True)

st.divider()

# ---------------- Top Skills ---------------- #
st.subheader("🧠 Top Skills Required")
if "required_skills" in df_filtered.columns and len(df_filtered) > 0:
    skills_series = df_filtered["required_skills"].dropna().str.split(", ").explode()
    top_skills = skills_series.value_counts().head(10).reset_index()
    top_skills.columns = ["Skill", "Count"]

    skills_fig = px.bar(
        top_skills, x="Count", y="Skill", orientation="h",
        color="Count", color_continuous_scale="Blues",
        title="Top 10 Skills"
    )
    skills_fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(skills_fig, use_container_width=True)
else:
    st.info("No skill data available for this selection.")

st.divider()

# ---------------- Remote Work Flexibility ---------------- #
st.subheader("🏠 Remote Work Flexibility")
if "remote_ratio" in df_filtered.columns and len(df_filtered) > 0:
    remote_data = df_filtered.groupby("remote_ratio").size().reset_index(name="count")
    remote_fig = px.bar(
        remote_data, x="count", y="remote_ratio", orientation="h",
        color="count", color_continuous_scale="Purples",
        labels={"remote_ratio": "Remote Work %", "count": "Number of Jobs"},
        title="Remote Work Ratio"
    )
    remote_fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(remote_fig, use_container_width=True)
else:
    st.info("No remote work data available.")
