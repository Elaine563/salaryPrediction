import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Insights", page_icon="📈", layout="wide")

# ---------------- Load Data ---------------- #
df = pd.read_csv("ai_job_dataset.csv")

# ---------------- Page Title & Description ---------------- #
st.title("📊 Job Market Insights Dashboard")
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
st.subheader("💡 Employee Count by Country & Top Skills")

col_map, col_skills = st.columns([3, 1])

# ---------------- Map: Count of People ---------------- #
with col_map:
    # st.markdown("#### ⚙️ Map of Employee Residence")

    # country_counts = df_filtered.groupby("employee_residence").size().reset_index(name="count")
    
    map_fig = px.choropleth(
        country_counts,
        locations="employee_residence",
        locationmode="country names",
        color="count",
        color_continuous_scale=["#FFFFFF","#FFC0CB","#B22222"],  
        hover_name="employee_residence",
        hover_data={"count": True},
    )
    
    map_fig.update_layout(
        title="Map of Employee Residence",  
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection_type="natural earth",
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        coloraxis_colorbar=dict(title="Number of People")
    )
    st.plotly_chart(map_fig, use_container_width=True)

# ---------------- Top 10 Skills as a Ranked List ---------------- #
with col_skills:
    st.markdown("#### 🧠 Top 10 Skills") 

    if "required_skills" in df_filtered.columns and len(df_filtered) > 0:
        skills_series = df_filtered["required_skills"].dropna().str.split(", ").explode()
        top_skills = skills_series.value_counts().head(10).reset_index()
        top_skills.columns = ["Skill", "Count"]

        # Display as numbered list with counts
        for idx, row in top_skills.iterrows():
            st.markdown(f"**{idx+1}. {row['Skill']}** — {row['Count']} jobs")
    else:
        st.info("No skill data available for this selection.")
        
# ---------------- Industry Radar Chart ---------------- #
st.subheader("🏭 Job Distribution by Industry")

# Create two columns: chart on left, description + table on right
col_chart, col_text_table = st.columns([3, 2])

# ---------------- Radar Chart ---------------- #
with col_chart:
    industry_counts = df_filtered["industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Count"]
    
    if not industry_counts.empty:
        fig_industry = px.line_polar(
            industry_counts,
            r="Count",
            theta="Industry",
            line_close=True,
            template="plotly_dark",
            color_discrete_sequence=["#B22222"]
        )
        fig_industry.update_traces(
            fill='toself',
            fillcolor='rgba(255, 76, 76, 0.3)',  # semi-transparent fill
            line=dict(color='#FF1A1A', width=3)  # darker line
        )
        fig_industry.update_layout(
            height=600,  # make chart taller
            width=800,   # make chart wider (optional)
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig_industry, use_container_width=True)
    else:
        st.warning("⚠️ No industry data available for this selection.")

# ---------------- Description + Ranking Table ---------------- #
with col_text_table:
    if not industry_counts.empty:
        top_industry = industry_counts.iloc[0]["Industry"]
        top_count = industry_counts.iloc[0]["Count"]
        st.markdown(
            f"""
            💡 **Insights for '{selected_job}'**:  
            - The **{top_industry}** industry has the highest number of job postings ({top_count} positions).  
            - Other industries show emerging demand; users can spot growing sectors easily.
            """
        )
        st.markdown("###### 📊 Industry Job Ranking")
        st.dataframe(industry_counts.reset_index(drop=True))
    else:
        st.info("No data available for this selection.")


# ---------------- Detailed Description ---------------- #
st.divider()
st.markdown(
    """
    ## 🔎 Dashboard Insights
    - The **map** highlights countries with the largest number of AI/ML employees. Darker red indicates a higher concentration of talent.
    - The **ranking list** on the right shows the top 10 skills most requested by employers for the selected job role.
    - The **Industry Radar Chart** shows which sectors demand AI skills the most.
    - By selecting different job titles, you can explore which skills are most demanded in different roles and where talent is concentrated globally.
    - This visualization helps both **job seekers** and **employers** understand market demand trends, identify skill gaps, and make data-driven decisions.
    """
)
