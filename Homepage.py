
import streamlit as st
from streamlit_lottie import st_lottie
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
	page_title="AI Career Navigator",
	page_icon="💼",
	layout="wide"
)

# -------------------- HELPER FUNCTIONS --------------------
def load_lottieurl(url: str):
	"""Safely load a Lottie animation from a given URL."""
	try:
		r = requests.get(url)
		if r.status_code != 200:
			return None
		return r.json()
	except Exception:
		return None

def clickable_card(title, description, lottie_url, page_path, key):
	"""Create a styled clickable card with optional animation and navigation."""
	card_style = """
	background-color: #f9fafc;
	padding: 20px;
	border-radius: 16px;
	box-shadow: 2px 4px 10px rgba(0,0,0,0.08);
	text-align: center;
	transition: all 0.2s ease-in-out;
	cursor: pointer;
	"""
	st.markdown(f"<div class='card' style='{card_style}'>", unsafe_allow_html=True)
	st.markdown(f"### {title}")
	st.markdown(description)

	if lottie_url:
		st_lottie(lottie_url, height=140, key=f"lottie_{key}")

	if st.button("→ Go", key=key, use_container_width=True):
		try:
			st.switch_page(page_path)
		except st.errors.StreamlitAPIException:
			st.error(f"⚠️ Page not found: `{page_path}`. Ensure it exists in the `pages/` folder.")
	st.markdown("</div>", unsafe_allow_html=True)

# -------------------- LOAD LOTTIE ANIMATIONS --------------------
lottie_ai = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_0yfsb3a1.json")
lottie_salary = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_t24tpvcu.json")
lottie_job = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_pprxh53t.json")
lottie_about = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_u4yrau.json")
lottie_cert = lottie_about  # Move animation from About Us to Cert Recommendations

# -------------------- TOP BANNER --------------------
st.image(
	"images/banner.png",  # path to your local banner image
	use_container_width=True
)

# -------------------- ADD HOVER EFFECT --------------------
st.markdown("""
<style>
.card:hover {
	transform: scale(1.04);
	box-shadow: 4px 8px 20px rgba(0,0,0,0.12);
}
button[kind="primary"] {
	border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown(
	"""
	<h1 style='text-align:center; color:#2F80ED;'>AI Career Navigator</h1>
	<div style='text-align:center; font-size:18px;'>
	Empowering your career with AI insights — Explore job markets, predict salaries, and plan smarter.
	</div>
	""",
	unsafe_allow_html=True
)
st.markdown("---")

# -------------------- ABOUT US ABOVE FEATURED TOOLS --------------------
st.subheader("ℹ️ About Us")
st.markdown(
	"""
	Learn more about our mission and the team behind **AI Career Navigator**.  
	Our goal is to empower students and professionals to make smarter career decisions using AI-driven insights.
	"""
)
# Direct Go button to About Us page
if st.button("→ Go to About Us", key="btn_about_direct"):
	try:
		st.switch_page("pages/1 🔍 About Us.py")
	except st.errors.StreamlitAPIException:
		st.error("⚠️ Page not found: `pages/AboutUs.py`. Ensure it exists in the `pages/` folder.")
st.markdown("---")

# -------------------- HERO SECTION --------------------
col1, col2 = st.columns([1.2, 1])

with col1:
	st.subheader("Explore the Future of Tech Careers")
	st.markdown(
		"""
		Welcome to **AI Career Navigator**, a platform designed to help students, professionals, and job seekers:
		- 📊 **Analyze real-world job market data**
		- 💰 **Predict potential salaries with AI**
		- 🧠 **Gain insights into the evolving AI industry**

		Click the cards below to navigate through our tools.
		"""
	)

with col2:
	if lottie_ai:
		st_lottie(lottie_ai, height=300, key="ai_animation")

st.markdown("---")

# -------------------- FEATURED TOOLS --------------------
st.subheader("✨ Featured Tools")

colA, colB, colC = st.columns(3)

with colA:
	clickable_card(
		"📊 Job Market Insights",
		"Dive into real-time hiring trends, skill demand, and industry shifts.",
		lottie_job,
		"pages/2 📊 Job Market Insights.py",
		"btn_job"
	)

with colB:
	clickable_card(
		"💰 Salary Prediction",
		"Estimate your potential income using AI-powered salary prediction models.",
		lottie_salary,
		"pages/3 💰 Salary Prediction.py",
		"btn_salary"
	)

with colC:
	clickable_card(
		"🎓 Cert Recommendations",
		"Get recommended courses and certifications to level up your skills.",
		lottie_cert,  # Animation moved here
		"pages/3 💰 Salary Prediction.py",
		"btn_cert"
	)

st.markdown("---")

# -------------------- FOOTER --------------------
st.markdown(
	"""
	<div style='text-align:center; color:gray; font-size:14px; margin-top:20px;'>
	© 2025 AI Career Navigator | Designed for Future Innovators 💡
	</div>
	""",
	unsafe_allow_html=True
)



