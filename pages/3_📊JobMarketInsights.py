import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="Job Market Insights", page_icon="📈", layout="wide")

# Load dataset
df = pd.read_csv("ai_job_dataset.csv")

# ---------------- Header ---------------- #
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>📊 Job Market Insights Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Explore global hiring and salary trends for AI-related job roles.</p>", unsafe_allow_html=True)
st.divider()

# ---------------- Filters ---------------- #
job_options = ["All"] + sorted(df["job_title"].unique().tolist())
selected_job = st.selectbox("🔍 Select Job Title:", job_options)
df_filtered = df.copy() if selected_job == "All" else df[df["job_title"] == selected_job]
st.info(f"Displaying insights for: **{selected_job}**")

# ---------------- Heatmap ---------------- #
with st.container():
    st.subheader("🌍 Employee Residence vs Company HQ")
    heatmap_data = df_filtered.groupby(["employee_residence", "company_location"]).size().reset_index(name="count")
    heatmap_fig = px.density_heatmap(
        heatmap_data,
        x="employee_residence",
        y="company_location",
        z="count",
        color_continuous_scale="Viridis",
        height=450
    )
    heatmap_fig.update_layout(xaxis_title="Employee Residence", yaxis_title="Company HQ")
    st.plotly_chart(heatmap_fig, use_container_width=True)

# ---------------- Pie Charts ---------------- #
with st.container():
    st.subheader("Demographics Overview")
    col1, col2, col3 = st.columns(3)
    pie_kwargs = {"hole":0.3, "color_discrete_sequence": px.colors.qualitative.Pastel}

    with col1:
        fig1 = px.pie(df_filtered, names="education_required", **pie_kwargs)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.pie(df_filtered, names="experience_level", **pie_kwargs)
        st.plotly_chart(fig2, use_container_width=True)
    with col3:
        fig3 = px.pie(df_filtered, names="company_size", **pie_kwargs)
        st.plotly_chart(fig3, use_container_width=True)

# ---------------- Salary Map ---------------- #
with st.container():
    st.subheader("🗺️ Average Salary by Employee Location")
    map_data = df_filtered.groupby("employee_residence")["salary_usd"].mean().reset_index()
    map_fig = px.choropleth(
        map_data,
        locations="employee_residence",
        locationmode="country names",
        color="salary_usd",
        color_continuous_scale="Plasma",
        title="Average Salary (USD)",
        height=450
    )
    st.plotly_chart(map_fig, use_container_width=True)

# ---------------- Word Cloud ---------------- #
with st.container():
    st.subheader("🧠 Top Skills Required")
    skills_text = " ".join(df_filtered["required_skills"].dropna().tolist())
    if skills_text.strip():
        wordcloud = WordCloud(background_color="#f5f5f5", colormap="viridis", width=800, height=300).generate(skills_text)
        fig, ax = plt.subplots(figsize=(10,4))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.warning("⚠️ No skill data available for this selection.")

# ---------------- Remote Work ---------------- #
with st.container():
    st.subheader("🏠 Remote Work Flexibility")
    remote_fig = px.bar(
        df_filtered.groupby("remote_ratio").size().reset_index(name="count"),
        x="count",
        y="remote_ratio",
        orientation="h",
        color="remote_ratio",
        color_continuous_scale="Blues",
        labels={"remote_ratio": "Remote Work %", "count": "Number of Jobs"},
        height=400
    )
    st.plotly_chart(remote_fig, use_container_width=True)
