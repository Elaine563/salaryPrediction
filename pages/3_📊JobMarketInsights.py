import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud

st.set_page_config(page_title="Job Market Insights", page_icon="📈", layout="wide")

# Load dataset
df = pd.read_csv("ai_job_dataset.csv")

# Sidebar filter
st.sidebar.header("Filters")
job_options = ["All"] + sorted(df["job_title"].unique())
selected_job = st.sidebar.selectbox("Select Job Title:", job_options)

df_filtered = df if selected_job == "All" else df[df["job_title"] == selected_job]

# Aggregate average salary by country
salary_data = df_filtered.groupby("employee_residence")["salary_usd"].mean().reset_index()

# Create choropleth map
map_fig = px.choropleth(
    salary_data,
    locations="employee_residence",
    locationmode="country names",
    color="salary_usd",
    color_continuous_scale="Viridis",  # Clean color scale
    hover_name="employee_residence",
    hover_data={"salary_usd":":,.0f"},
    title=f"🌍 Average AI Job Salary by Country ({selected_job})",
)

# Improve layout
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

# Display map in Streamlit
st.plotly_chart(map_fig, use_container_width=True)
