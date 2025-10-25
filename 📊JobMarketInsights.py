import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="Job Market Insights", page_icon="📈", layout="wide")

# Load dataset
df = pd.read_csv("ai_job_dataset.csv")

st.title("📊 Job Market Insights Dashboard")
st.write("Explore global hiring and salary trends for AI-related job roles.")

# ========== Filter Section ========== #
job_options = ["All"] + sorted(df["job_title"].unique().tolist())
selected_job = st.selectbox("🔍 Select Job Title:", job_options)

# Apply filter
df_filtered = df.copy() if selected_job == "All" else df[df["job_title"] == selected_job]

st.info(f"Displaying insights for: **{selected_job}**")

st.divider()

# ========== Heatmap ========== #
st.subheader("🌍 Employee Residence vs Company HQ Location")
heatmap_data = df_filtered.groupby(["employee_residence", "company_location"]).size().reset_index(name="count")

heatmap_fig = px.density_heatmap(
    heatmap_data,
    x="employee_residence",
    y="company_location",
    z="count",
    color_continuous_scale="Viridis",
    height=450,
)
heatmap_fig.update_layout(xaxis_title="Employee Residence", yaxis_title="Company HQ Location")
st.plotly_chart(heatmap_fig, use_container_width=True)

st.divider()

# ✅ 3 PIE CHARTS
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🎓 Education Level")
    fig1 = px.pie(df_filtered, names="education_required", hole=0.3,
                  color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("💼 Experience Level")
    fig2 = px.pie(df_filtered, names="experience_level", hole=0.3,
                  color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.subheader("🏢 Company Size")
    fig3 = px.pie(df_filtered, names="company_size", hole=0.3,
                  color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ========== Salary Map ========== #
st.subheader("🗺️ Global Salary by Employee Location")
map_data = df_filtered.groupby("employee_residence")["salary_usd"].mean().reset_index()

map_fig = px.choropleth(
    map_data,
    locations="employee_residence",
    locationmode="country names",
    color="salary_usd",
    color_continuous_scale="Plasma",
    title="Average Salary (USD)",
    height=450,
)
st.plotly_chart(map_fig, use_container_width=True)

st.divider()

# ========== Word Cloud: Required Skills ========== #
st.subheader("🧠 Top Skills Required")

skills_text = " ".join(df_filtered["required_skills"].dropna().tolist())

if skills_text.strip():
    wordcloud = WordCloud(background_color="white", width=800, height=300).generate(skills_text)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)
else:
    st.warning("⚠️ No skill data available for this selection.")

st.divider()

# ========== Bar Chart for Remote Work Ratio ========== #
st.subheader("🏠 Remote Work Flexibility")

remote_fig = px.bar(
    df_filtered,
    x="remote_ratio",
    color="remote_ratio",
    title="Remote Work Allowance (%)",
    labels={"remote_ratio": "Remote Work %"},
    height=400,
)
st.plotly_chart(remote_fig, use_container_width=True)

st.caption("📊 Data-driven insights update instantly based on selected job title.")
