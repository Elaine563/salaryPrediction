import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Insights", page_icon="📈", layout="wide")

# ---------------- Load Data ---------------- #
df = pd.read_csv("ai_job_dataset.csv")

# ---------------- Page Title & Description ---------------- #
st.title("📊 Job Market Insights Dashboard", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align: left; font-size:16px;'>
    Explore the global distribution of AI-related job positions and discover the most in-demand skills in the market.
    Select a job title below to filter the insights. The map shows the number of employees per country, and the ranking
    on the right lists the top 10 most requested skills for the selected role.
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

# ---------------- Map and Top Skills Side by Side ---------------- #
st.subheader("🌍 Employee Count by Country & Top Skills")

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

# ---------------- Top 10 Skills as a Ranked List ---------------- #
with col_skills:
    st.markdown("### 🧠 Top 10 Skills")
    if "required_skills" in df_filtered.columns and len(df_filtered) > 0:
        skills_series = df_filtered["required_skills"].dropna().str.split(", ").explode()
        top_skills = skills_series.value_counts().head(10).reset_index()
        top_skills.columns = ["Skill", "Count"]

        # Display as numbered list with counts
        for idx, row in top_skills.iterrows():
            st.markdown(f"**{idx+1}. {row['Skill']}** — {row['Count']} jobs")
    else:
        st.info("No skill data available for this selection.")

# ---------------- Detailed Description ---------------- #
st.divider()
st.markdown(
    """
    ## 🔎 Dashboard Insights
    - The **map** highlights countries with the largest number of AI/ML employees. Darker red indicates a higher concentration of talent.
    - The **ranking list** on the right shows the top 10 skills most requested by employers for the selected job role.
    - By selecting different job titles, you can explore which skills are most demanded in different roles and where talent is concentrated globally.
    - This visualization helps both **job seekers** and **employers** understand market demand trends, identify skill gaps, and make data-driven decisions.
    """
)
