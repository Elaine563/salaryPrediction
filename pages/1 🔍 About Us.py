import os
import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="🔍 About Us | Future of Jobs Dashboard", page_icon="👥", layout="wide")

# -------------------- TOP BANNER --------------------
st.image(
    "images/aboutUs.jpg",  
    use_container_width=True  # spans the full width of the page/container
)

# --- TEAM SECTION ---
st.header("Meet the Team")

base_image_path = os.path.join(os.path.dirname(__file__), "..", "images")

team_members = [
    {
        "name": "Lim Jun Zhe",
        "role": "Project Lead & Data Scientist",
        "bio": "Loves transforming data into actionable insights. Passionate about machine learning, storytelling, and solving real-world problems.",
        "skills": "Python, Machine Learning, Data Visualization, SQL",
        "linkedin": "https://www.linkedin.com/in/lim-jun-zhe-nathan-6932aa25a/",
        "github": "https://github.com/Nathannnn71",
        "image": os.path.join(base_image_path, "junzhe.png")
    },
    {
        "name": "Wen Ting",
        "role": "Full Stack Developer",
        "bio": "Enjoys crafting smooth, interactive web experiences that connect people and data intuitively.",
        "skills": "Streamlit, React, Python, PostgreSQL",
        "linkedin": "https://www.linkedin.com/in/tingwen-goh/",
        "github": "https://github.com/wmint9220",
        "image": os.path.join(base_image_path, "wenting.png")
    },
    {
        "name": "Elaine Wong Jing Wern",
        "role": "Data Scientist + UI/UX Designer",
        "bio": "Contribute to dashboard designs, user-centered interfaces that make data exploration enjoyable and accessible.",
        "skills": "Streamlit, React, Python, User Research, Prototyping, C++",
        "linkedin": "www.linkedin.com/in/elaine-wong-178aaa290",
        "github": "https://github.com/Elaine563",
        "image": os.path.join(base_image_path, "elaine.jpg")
    },
    {
        "name": "Isya",
        "role": "Data Analyst",
        "bio": "Passionate about uncovering patterns in data and turning them into stories people can see and understand.",
        "skills": "Pandas, Data Mining, Tableau, Statistics",
        "linkedin": "https://www.linkedin.com/in/laurisya-nagarajan-b85089354/",
        "github": "https://github.com/Isya1406",
        "image": os.path.join(base_image_path, "isya.png")
    }
]

# --- INDIVIDUAL MEMBER CARDS (website-style layout) ---
for member in team_members:
    st.markdown("---")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(member["image"], width=200)
    with col2:
        st.markdown(f"### {member['name']}")
        st.markdown(f"**{member['role']}**")
        st.write(member["bio"])
        st.markdown(f"**Skills:** {member['skills']}")
        st.markdown(f"[🔗 LinkedIn]({member['linkedin']}) | [💻 GitHub]({member['github']})")

st.markdown("---")

# --- OUR MISSION ---
st.header("Our Mission")
st.markdown("""
At **Future of Jobs Dashboard**, we aim to bridge the gap between data and decision-making in today’s dynamic job market.  
Our goal is to empower **students, job seekers, and organizations** with data-driven insights about the evolving landscape of work —  
from salaries and in-demand skills to market trends and opportunities.
""")

st.markdown("---")

# --- OUR STORY ---
st.header("Our Story")
st.markdown("""
It all began with a shared curiosity among a group of university students who wanted to understand how technology is transforming the job market.  
During an internship program at **TCS iON**, our team decided to take on a challenge — to create a **Salary Prediction Dashboard** that could  
help people explore **career insights** through data visualization and machine learning.

What started as a simple project idea soon turned into a passion project.  
We combined our unique skills — from **data science** to **UI/UX design** — to create something meaningful:  
a platform that doesn’t just show numbers, but tells stories about people, jobs, and the future of work.
""")

st.markdown("---")



# --- TECHNOLOGY STACK ---
st.header("Tools We Used")
st.markdown("""
We’ve used a modern, open-source tech stack to make our dashboard interactive, scalable, and visually engaging.
""")

tech_cols = st.columns(4)
techs = [
    ("🐍 Python", "The brain behind all data analysis and modeling."),
    ("📊 Streamlit", "Our favorite tool for turning data into web apps."),
    ("📈 Plotly", "For smooth, interactive visualizations."),
    ("🗃️ Pandas", "Used for all data wrangling and cleaning.")
]
for col, (title, desc) in zip(tech_cols, techs):
    with col:
        st.subheader(title)
        st.write(desc)

st.markdown("---")

# --- DATA SOURCE ---
st.header("📊 Data Source")
st.markdown("""
This project uses the **Global AI Job Market & Salary Trends 2025** dataset from Kaggle,  
containing job postings, salary insights, skill requirements, and employment trends across the world.  

🔗 [**Kaggle Dataset: Global AI Job Market and Salary Trends 2025**](https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025/data)
""")

st.markdown("---")

# --- CONTACT SECTION ---
st.header("Get in Touch")
st.markdown("We’d love to hear from you — whether it’s feedback, collaboration ideas, or just a hello!")

contact_cols = st.columns(3)
with contact_cols[0]:
    st.markdown("### Email")
    st.write("team@futureofjobs.com")
with contact_cols[1]:
    st.markdown("### Website")
    st.write("[www.futureofjobs.com](https://www.futureofjobs.com)")
with contact_cols[2]:
    st.markdown("### Feedback")
    st.write("Your thoughts help us grow ❤️")

with st.expander("📝 Send Us Feedback"):
    with st.form("feedback_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message", height=150)
        if st.form_submit_button("Send Feedback"):
            st.success("Thank you for your feedback! We'll get back to you soon. 🎉")

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; padding: 20px; color: #777;">
    <p>© 2024 Future of Jobs Dashboard — Created by Our Team with ❤️</p>
</div>
""", unsafe_allow_html=True)
