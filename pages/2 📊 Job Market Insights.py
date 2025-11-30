import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Job Market Insights | Future of Jobs Dashboard", page_icon="📈", layout="wide")

# ---------------- Load Data ---------------- #
df = pd.read_csv("ai_job_dataset.csv")

# ---------------- Page Title & Description ---------------- #
st.title("Job Market Insights Dashboard")
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
conversion_rates = {"USD": 1, "MYR": 4.13}
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

        CURRENCY_RATES = { 
            
            "USD": {"symbol": "$", "rate": 1.0, "name": "US Dollar"}, 
            "MYR": {"symbol": "RM", "rate": 4.13, "name": "Malaysian Ringgit"}, 
        }
        currency_symbol = CURRENCY_RATES[currency_type]['symbol']

        # Get median and count safely with fallback to 0
        def get_stat(level, col):
            if level in exp_stats['experience_level'].values:
                return exp_stats.loc[exp_stats['experience_level']==level, col].values[0]
            return 0

        st.markdown(f"""
        The violin plot above shows the salary distribution for different experience levels:
        - <b>EN (Entry-Level)</b>: Median salary is {currency_symbol}{get_stat('EN','median'):.0f}, with {get_stat('EN','count')} records.
        - <b>SE (Senior)</b>: Median salary is {currency_symbol}{get_stat('SE','median'):.0f}, with {get_stat('SE','count')} records.
        - <b>MI (Mid-Level)</b>: Median salary is {currency_symbol}{get_stat('MI','median'):.0f}, with {get_stat('MI','count')} records.
        - <b>EX (Executive)</b>: Median salary is {currency_symbol}{get_stat('EX','median'):.0f}, with {get_stat('EX','count')} records.
        <br><br>
        Senior and Executive levels show higher median and maximum salaries, while Entry-Level and Mid-Level have lower ranges. This highlights the impact of experience on salary growth in AI-related roles.
        """, unsafe_allow_html=True)


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

        st.markdown("<b>Company Size Salary Statistics:</b>", unsafe_allow_html=True)
        st.dataframe(company_salary)
        CURRENCY_RATES = { "USD": {"symbol": "$", "rate": 1.0, "name": "US Dollar"}, "MYR": {"symbol": "RM", "rate": 4.13, "name": "Malaysian Ringgit"}, }
        currency_symbol = CURRENCY_RATES[currency_type]['symbol']

        # Extract salary values safely
        salary_L = company_salary.loc[company_salary['company_size']=='L','converted_salary'].values
        salary_M = company_salary.loc[company_salary['company_size']=='M','converted_salary'].values
        salary_S = company_salary.loc[company_salary['company_size']=='S','converted_salary'].values

        salary_L = salary_L[0] if len(salary_L) > 0 else 0
        salary_M = salary_M[0] if len(salary_M) > 0 else 0
        salary_S = salary_S[0] if len(salary_S) > 0 else 0
        top_salary = company_salary['converted_salary'].max()

        st.write("The chart above compares the average salary across different company sizes.")
        st.write(f"Large companies (L) have an average salary of **{currency_symbol}{salary_L:,.0f}**.")
        st.write(f"Medium companies (M) offer around **{currency_symbol}{salary_M:,.0f}**.")
        st.write(f"Small companies (S) provide an average salary of **{currency_symbol}{salary_S:,.0f}**.")
        st.write(f"Overall, larger companies tend to offer higher pay, with the highest recorded salary reaching **{currency_symbol}{top_salary:,.0f}**.")
        st.write("Smaller companies may offer lower averages but often provide other advantages such as flexibility or broader roles.")



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

        CURRENCY_RATES = { "USD": {"symbol": "$", "rate": 1.0, "name": "US Dollar"}, "MYR": {"symbol": "RM", "rate": 4.13, "name": "Malaysian Ringgit"}, }
        currency_symbol = CURRENCY_RATES[currency_type]['symbol']

        max_salary = heatmap_data['converted_salary'].max() if 'converted_salary' in heatmap_data.columns else 0
        min_salary = heatmap_data['converted_salary'].min() if 'converted_salary' in heatmap_data.columns else 0

        st.write(
            "The heatmap above shows the highest average salary for Executive-Level experience and Contract employment at",
            f"{currency_symbol}{max_salary:,.0f}")
        
        st.write(
            "This may suggest that Contract employment type is employed for certain projects and makes more frequent top-level decisions with Executive-Level positions. "
            "On the other hand, the lowest average salary for Entry-Level experience and Part-Time employment is at",
            f"{currency_symbol}{min_salary:,.0f}")

        st.write(
            "This may suggest that Part-Time employment type is employed for less demanding and basic workloads in which they may also be supervised at the Entry-Level position."
        )


    else:
        st.warning("Years of experience or education level data is not available.")


