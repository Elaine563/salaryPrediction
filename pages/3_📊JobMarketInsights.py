import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Insights", page_icon="📈", layout="wide")

# ---------------- Load Data ---------------- #
df = pd.read_csv("ai_job_dataset.csv")

# ---------------- Page Title & Description ---------------- #
st.markdown("<h1 style='text-align: center; color: #B22222;'>📊 Job Market Insights Dashboard</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align: center; font-size:16px;'>
    This dashboard visualizes the global distribution of AI-related job positions and highlights the 
    most in-demand skills for professionals in the AI/ML job market. Use the filter below to select a specific job title 
    or explore the overall trends across all roles. The map shows the number of employees per country, and the ranking 
    on the right lists the top 10 most required skills based on the current selection.
    </p>
    """, unsafe_allow_html=True
)

# ---------------- Filter Section in the Center ---------------- #
st.markdown("### 🔍 Filter by Job Title")
job_options = ["All"] + sorted(df["job_title"].unique())
selected_job = st.selectbox("", job_options, index=0, key="job_filter")

df_filtered = df if selected_job == "All" else df[df["job_title"] == selected_job]

st.info(f"Displaying insights for: **{selected_job}**. Total records: {len(df_filtered)}")

st.divider()

# ---------------- Map and Skills Side by Side ---------------- #
st.subheader("🌍 Employee Count by Country & Top Skills")

# Layout: map on left, top skills on right
col_map, col_skills = st.columns([3, 1])

# ---------------- Map: Count of People ---------------- #
with col_map:
    country_counts = df_filtered.groupby("employee_residence").size().reset_index(name="count")
    
    map_fig = px.choropleth(
        country_counts,
        locations="employee_residence",
        locationmode="country names",
        color="count",
        color_continuous_scale=["#B22222","#FF69B4","#FFFFFF"],  # red → pink → white
        hover_name="employee_residence",
        hover_data={"count": True},
        title="Number of Employees per Country",
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
        coloraxis_colorbar=dict(title="Number of People")
    )
    st.plotly_chart(map_fig, use_container_width=True)

# ---------------- Top 10 Skills Ranking ---------------- #
with col_skills:
    st.markdown("### 🧠 Top 10 Skills")
    if "required_skills" in df_filtered.columns and len(df_filtered) > 0:
        skills_series = df_filtered["required_skills"].dropna().str.split(", ").explode()
        top_skills = skills_series.value_counts().head(10).reset_index()
        top_skills.columns = ["Skill", "Count"]

        skills_fig = px.bar(
            top_skills, x="Count", y="Skill", orientation="h",
            color="Count", color_continuous_scale="Reds",
        )
        skills_fig.update_layout(yaxis=dict(autorange="reversed"), showlegend=False, margin=dict(l=0, r=0, t=20, b=0))
        st.plotly_chart(skills_fig, use_container_width=True)
    else:
        st.info("No skill data available for this selection.")

# ---------------- Detailed Description ---------------- #
st.divider()
st.markdown(
    """
    ## 🔎 Dashboard Insights
    - The **map** highlights countries with the largest number of AI/ML employees. Darker red indicates a higher concentration of talent.
    - The **ranking chart** on the right lists the top 10 skills most frequently requested by employers for the selected job role.
    - By selecting different job titles, you can explore which skills are most demanded in different roles and where talent is concentrated globally.
    - This visualization helps both **job seekers** and **employers** understand market demand trends, identify skill gaps, and make data-driven decisions.
    """
)
