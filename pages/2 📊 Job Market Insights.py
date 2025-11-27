import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Job Market Insights | Future of Jobs Dashboard", page_icon="📈", layout="wide")

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

# ---------------- Currency Selection ---------------- #
currency_type = st.radio(
    "**Currency Selection**",
    ["USD", "MYR"],
    captions=["United States Dollar", "Malaysian Ringgit"],
    horizontal=True
)
conversion_rates = {"USD": 1, "MYR": 4.5}
conversion_rate = conversion_rates[currency_type]
if "salary_usd" in df.columns:
    df["converted_salary"] = df["salary_usd"] * conversion_rate

# ---------------- Tabs for EDA ---------------- #
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Employee Count & Top Skills",
    "Job Distribution by Industry",
    "Salary Distribution by Experience Level",
    "Average Salary by Company Size",
    "Salary by Years of Experience & Education"
])

# ---------------- Tab 1: Employee Count & Top Skills ---------------- #
with tab1:
    st.subheader("💡 Employee Count by Country & Top Skills")

    # ---------------- Filter by Job Title ---------------- #
    st.markdown("### 🔍 Filter by Job Title")
    job_options = ["All"] + sorted(df["job_title"].unique())
    selected_job = st.selectbox("", job_options, index=0, key="job_filter")

    df_filtered = df if selected_job == "All" else df[df["job_title"] == selected_job]

    st.info(f"Displaying insights for: **{selected_job}**. Total records: {len(df_filtered)}")

    col_map, col_skills = st.columns([3, 1])

    # ---------------- Map: Count of People ---------------- #
    with col_map:
        st.markdown("#### ⚙️ Map of Employee Residence")

        country_counts = df_filtered.groupby("employee_residence").size().reset_index(name="count")
        map_fig = px.choropleth(
            country_counts,
            locations="employee_residence",
            locationmode="country names",
            color="count",
            color_continuous_scale=["#FFFFFF", "#FFC0CB", "#B22222"],
            hover_name="employee_residence",
            hover_data={"count": True},
        )
        map_fig.update_layout(
            geo=dict(
                showframe=True,
                showcoastlines=True,
                projection_type="natural earth",
                bgcolor="rgba(0,0,0,0)"
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(title="Number of People")
        )
        st.plotly_chart(map_fig, width='stretch')

        st.write(
            "The map above highlights the global distribution of AI/ML employees. Countries with darker shades of red indicate a higher concentration of talent, "
            "suggesting regions with significant AI-related activities. For example, countries like the United States and China may have a higher density of AI professionals "
            "due to their advanced technological infrastructure and investment in AI research. Conversely, lighter shades represent regions with fewer AI professionals, "
            "indicating potential opportunities for growth and development in the AI sector."
        )

    # ---------------- Top 10 Skills as a Ranked List ---------------- #
    with col_skills:
        st.markdown("#### 🧠 Top 10 Skills")

        if "required_skills" in df_filtered.columns and len(df_filtered) > 0:
            skills_series = df_filtered["required_skills"].dropna().str.split(", ").explode()
            top_skills = skills_series.value_counts().head(10).reset_index()
            top_skills.columns = ["Skill", "Count"]

            for idx, row in top_skills.iterrows():
                st.markdown(f"**{idx+1}. {row['Skill']}** — {row['Count']} jobs")
        else:
            st.info("No skill data available for this selection.")

# ---------------- Tab 2: Job Distribution by Industry ---------------- #
with tab2:
    st.subheader("🏭 Job Distribution by Industry")

    col_chart, col_text_table = st.columns([3, 2])

    # ---------------- Radar Chart ---------------- #
    with col_chart:
        industry_counts = df["industry"].value_counts().reset_index()
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
                fillcolor='rgba(255, 76, 76, 0.3)',
                line=dict(color='#FF1A1A', width=3)
            )
            fig_industry.update_layout(
                height=600,
                width=800,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_industry, width='stretch')

            st.write(
                "The radar chart above illustrates the distribution of AI-related jobs across various industries. Industries such as Technology and Healthcare dominate the chart, "
                "indicating their significant demand for AI professionals. This trend reflects the growing integration of AI in these sectors, where it is used to enhance operational efficiency, "
                "drive innovation, and improve decision-making processes. Conversely, industries with smaller areas on the chart may represent emerging opportunities for AI applications, "
                "highlighting potential areas for growth and investment."
            )
        else:
            st.warning("⚠️ No industry data available for this selection.")

# ---------------- Tab 3: Salary Distribution by Experience Level ---------------- #
with tab3:
    st.subheader("📊 Salary Distribution by Experience Level")

    if "experience_level" in df.columns:
        violin_fig = px.violin(
            df,
            x="experience_level",
            y="converted_salary",
            box=True,
            points="all",
            color="experience_level",
            color_discrete_sequence=px.colors.qualitative.Set2,
            labels={"experience_level": "Experience Level", "converted_salary": f"Salary ({currency_type})"}
        )
        st.plotly_chart(violin_fig, width='stretch')

        # --- Enhanced Explanation with Statistics --- #
        exp_stats = df.groupby("experience_level")['converted_salary'].agg(['count','mean','median','min','max']).reset_index()
        st.markdown("<b>Statistics by Experience Level:</b>", unsafe_allow_html=True)
        st.dataframe(exp_stats)
        st.markdown(
            """
            The violin plot above shows the salary distribution for different experience levels:
            - <b>EN (Entry-Level)</b>: Median salary is ${:.0f}, with {} records.
            - <b>SE (Senior)</b>: Median salary is ${:.0f}, with {} records.
            - <b>MI (Mid-Level)</b>: Median salary is ${:.0f}, with {} records.
            - <b>EX (Executive)</b>: Median salary is ${:.0f}, with {} records.
            <br><br>
            Senior and Executive levels show higher median and maximum salaries, while Entry-Level and Mid-Level have lower ranges. This highlights the impact of experience on salary growth in AI-related roles.
            """.format(
                exp_stats.loc[exp_stats['experience_level']=='EN','median'].values[0] if 'EN' in exp_stats['experience_level'].values else 0,
                exp_stats.loc[exp_stats['experience_level']=='EN','count'].values[0] if 'EN' in exp_stats['experience_level'].values else 0,
                exp_stats.loc[exp_stats['experience_level']=='SE','median'].values[0] if 'SE' in exp_stats['experience_level'].values else 0,
                exp_stats.loc[exp_stats['experience_level']=='SE','count'].values[0] if 'SE' in exp_stats['experience_level'].values else 0,
                exp_stats.loc[exp_stats['experience_level']=='MI','median'].values[0] if 'MI' in exp_stats['experience_level'].values else 0,
                exp_stats.loc[exp_stats['experience_level']=='MI','count'].values[0] if 'MI' in exp_stats['experience_level'].values else 0,
                exp_stats.loc[exp_stats['experience_level']=='EX','median'].values[0] if 'EX' in exp_stats['experience_level'].values else 0,
                exp_stats.loc[exp_stats['experience_level']=='EX','count'].values[0] if 'EX' in exp_stats['experience_level'].values else 0,
            ), unsafe_allow_html=True
        )
    else:
        st.warning("Experience level data is not available.")

# ---------------- Tab 4: Average Salary by Company Size ---------------- #
with tab4:
    st.subheader("💰 Average Salary by Company Size")

    if "company_size" in df.columns:
        company_salary = df.groupby("company_size")["converted_salary"].mean().reset_index()
        bar_fig = px.bar(
            company_salary,
            x="company_size",
            y="converted_salary",
            color="converted_salary",
            color_continuous_scale="Blues",
            labels={"company_size": "Company Size", "converted_salary": f"Average Salary ({currency_type})"}
        )
        st.plotly_chart(bar_fig, width='stretch')
        # --- Enhanced Explanation with Statistics --- #
        st.markdown("<b>Company Size Salary Statistics:</b>", unsafe_allow_html=True)
        st.dataframe(company_salary)
        st.markdown(
            """
            The bar chart shows the average salary by company size:
            - <b>L (Large)</b>: Average salary is ${:.0f}
            - <b>M (Medium)</b>: Average salary is ${:.0f}
            - <b>S (Small)</b>: Average salary is ${:.0f}
            <br><br>
            Larger companies tend to offer higher salaries, with large companies averaging ${:.0f}. Small companies show more variability and may offer lower average salaries, but can provide other benefits such as flexibility or broader responsibilities.
            """.format(
                company_salary.loc[company_salary['company_size']=='L','converted_salary'].values[0] if 'L' in company_salary['company_size'].values else 0,
                company_salary.loc[company_salary['company_size']=='M','converted_salary'].values[0] if 'M' in company_salary['company_size'].values else 0,
                company_salary.loc[company_salary['company_size']=='S','converted_salary'].values[0] if 'S' in company_salary['company_size'].values else 0,
                company_salary['converted_salary'].max()
            ), unsafe_allow_html=True
        )
    else:
        st.warning("Company size data is not available.")

# ---------------- Tab 5: Salary by Years of Experience & Education ---------------- #
with tab5:
    st.subheader("📚 Salary by Years of Experience & Education")

    if "years_experience" in df.columns and "education_required" in df.columns:
        heatmap_data = df.groupby(["years_experience", "education_required"])["converted_salary"].mean().reset_index()
        heatmap_pivot = heatmap_data.pivot(index="education_required", columns="years_experience", values="converted_salary")

        heatmap_fig = px.imshow(
            heatmap_pivot,
            color_continuous_scale="Turbo",  # Use a distinct color scale
            labels={"x": "Years of Experience", "y": "Education Level", "color": f"Average Salary ({currency_type})"},
            text_auto=True  # Annotate each cell with salary values
        )
        heatmap_fig.update_layout(
            title="Average Salary by Years of Experience & Education",
            xaxis_title="Years of Experience",
            yaxis_title="Education Level",
            coloraxis_colorbar=dict(title=f"Average Salary ({currency_type})")
        )
        st.plotly_chart(heatmap_fig, width='stretch')

        # Add paragraph explanation
        st.markdown(
            """
            <div style='font-size:18px; font-family:Arial; color:#F8F8F8; font-weight:600;'>
            The heatmap above shows the highest average salary at <span style='color:#FFD700;'>${max_salary:,.0f}</span> for Executive-Level experience and Contract employment.<br>
            This may suggest that Contract employment type is employed for certain projects and makes more frequent top-level decisions with Executive-Level positions.<br>
            On the other hand, the lowest average salary is at <span style='color:#FF6347;'>${min_salary:,.0f}</span> for Entry-Level experience and Part-Time employment.<br>
            This may suggest that Part-Time employment type is employed for less demanding and basic workloads in which they may also be supervised at the Entry-Level position.
            </div>
            """.format(
                max_salary=heatmap_data['converted_salary'].max() if 'converted_salary' in heatmap_data.columns else 0,
                min_salary=heatmap_data['converted_salary'].min() if 'converted_salary' in heatmap_data.columns else 0
            ), unsafe_allow_html=True
        )
    else:
        st.warning("Years of experience or education level data is not available.")


