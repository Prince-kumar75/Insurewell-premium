import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000/predict")

st.set_page_config(
    page_title="InsureWell | Premium Predictor",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #0f2a4a;
    --teal: #5f8ea3;
    --teal-dark: #4a7a90;
    --soft: #f3f6f9;
    --muted: #6b7a8c;
}

html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp { background: #ffffff; }
header[data-testid="stHeader"], footer, #MainMenu { display: none; }
.block-container { padding: 1.2rem 2.5rem 3rem 2.5rem; max-width: 1250px; }

/* ---------- hero ---------- */
.hero {
    position: relative;
    background: linear-gradient(135deg, #7ba3b5 0%, #5a8aa0 55%, #4a7a90 100%);
    border-radius: 22px;
    padding: 22px 38px 60px 38px;
    color: #fff;
    overflow: hidden;
    min-height: 430px;
}
.hero::before, .hero::after {
    content: ""; position: absolute; border-radius: 50%;
    background: rgba(255,255,255,0.08);
}
.hero::before { width: 380px; height: 380px; right: -60px; top: -80px; }
.hero::after  { width: 260px; height: 260px; right: 160px; bottom: -120px; }

.nav {
    display: flex; align-items: center; justify-content: space-between;
    background: rgba(255,255,255,0.18); backdrop-filter: blur(6px);
    border-radius: 999px; padding: 10px 22px; position: relative; z-index: 2;
}
.nav .logo { font-weight: 800; font-size: 18px; letter-spacing: .3px; }
.nav .links { display: flex; gap: 26px; font-size: 13px; font-weight: 500; opacity: .95; }
.nav .cta {
    background: var(--navy); color: #fff; font-size: 12px; font-weight: 600;
    padding: 8px 18px; border-radius: 999px;
}

.hero .tag {
    margin-top: 38px; display: inline-flex; align-items: center; gap: 8px;
    font-size: 12px; font-weight: 500; position: relative; z-index: 2;
}
.hero .tag .dot {
    width: 22px; height: 22px; border-radius: 50%; background: #fff; display: inline-block;
}
.hero h1 {
    font-size: clamp(64px, 11vw, 138px); line-height: .95; font-weight: 800;
    letter-spacing: -2px; margin: 10px 0 18px 0; color: #fff; position: relative; z-index: 2;
}
.hero p.sub {
    max-width: 440px; font-size: 14px; line-height: 1.6; opacity: .92;
    position: relative; z-index: 2; margin-bottom: 20px;
}
.hero .btn {
    display: inline-block; background: var(--navy); color: #fff; font-size: 12px;
    font-weight: 600; padding: 10px 22px; border-radius: 999px; position: relative; z-index: 2;
}
.hero .doctor {
    position: absolute; right: 70px; bottom: 0; font-size: 270px; line-height: 1; z-index: 1;
    filter: drop-shadow(0 12px 18px rgba(0,0,0,.18));
}
.hero .float-card {
    position: absolute; left: 38px; bottom: 22px; z-index: 3; background: #fff; color: var(--navy);
    border-radius: 14px; padding: 10px 16px; font-size: 12px; font-weight: 600;
    box-shadow: 0 8px 24px rgba(15,42,74,.18);
}
.hero .float-card span { display:block; font-weight:400; color: var(--muted); font-size: 11px; }

/* ---------- intro ---------- */
.intro { display: flex; align-items: center; gap: 60px; padding: 60px 10px 30px 10px; }
.intro .big { font-size: 110px; font-weight: 300; color: var(--navy); line-height: 1; white-space: nowrap; }
.intro h3 { font-size: 28px; font-weight: 500; color: var(--navy); line-height: 1.3; margin: 0 0 12px 0; }
.intro p { color: var(--muted); font-size: 13px; line-height: 1.7; max-width: 520px; }

/* ---------- section titles ---------- */
.section-title { font-size: 26px; font-weight: 700; color: var(--navy); margin: 30px 0 4px 0; }
.section-sub { color: var(--muted); font-size: 13px; margin-bottom: 18px; }

/* ---------- form widgets ---------- */
div[data-testid="stForm"] {
    background: var(--soft); border: none; border-radius: 20px; padding: 28px 28px 14px 28px;
}
label, .stMarkdown label p { color: var(--navy) !important; font-weight: 600 !important; font-size: 13px !important; }
div[data-baseweb="input"], div[data-baseweb="select"] > div {
    border-radius: 12px !important; background: #fff !important;
}
.stButton > button, div[data-testid="stFormSubmitButton"] > button {
    background: var(--navy); color: #fff; border: none; border-radius: 999px;
    padding: .65rem 2.2rem; font-weight: 600; font-size: 14px; transition: .2s;
}
.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    background: var(--teal-dark); color: #fff; border: none;
}

/* ---------- result ---------- */
.result {
    background: linear-gradient(135deg, #5a8aa0, #4a7a90); color: #fff;
    border-radius: 20px; padding: 30px 32px; margin-top: 10px;
}
.result .label { font-size: 12px; opacity: .85; text-transform: uppercase; letter-spacing: 1.2px; }
.result .value { font-size: 52px; font-weight: 800; margin: 4px 0 6px 0; text-transform: capitalize; }
.result .note { font-size: 13px; opacity: .9; }

.metric-card {
    background: #fff; border: 1px solid #e6ebf0; border-radius: 16px; padding: 18px 20px;
}
.metric-card .m-val { font-size: 26px; font-weight: 700; color: var(--navy); }
.metric-card .m-lab { font-size: 12px; color: var(--muted); }

/* ---------- stats strip ---------- */
.stats { display: flex; gap: 18px; margin-top: 46px; }
.stats .card {
    flex: 1; background: var(--soft); border-radius: 18px; padding: 24px 26px;
}
.stats .num { font-size: 40px; font-weight: 700; color: var(--navy); }
.stats .lab { font-size: 12px; color: var(--muted); }

.footer { text-align:center; color: var(--muted); font-size: 12px; margin-top: 50px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- hero
st.markdown(
    """
<div class="hero">
  <div class="nav">
    <div class="logo">✚ InsureWell</div>
    <div class="links"><span>Home</span><span>About</span><span>Plans</span><span>Blog</span><span>Contact</span></div>
    <div class="cta">Get a quote</div>
  </div>
  <div class="tag"><span class="dot"></span> Smart health insurance estimates</div>
  <h1>PREMIUM</h1>
  <p class="sub">Together, delivering transparent and instant insurance premium
  predictions powered by machine learning. Share a few details and see your category.</p>
  <span class="btn">Predict now ↓</span>
  <div class="doctor">🩺</div>
  <div class="float-card">AI risk assessment<span>Instant · Private · Free</span></div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- intro
st.markdown(
    """
<div class="intro">
  <div class="big">25+</div>
  <div>
    <h3>Trusted by thousands — one purpose, fair and transparent premiums.</h3>
    <p>Our model weighs your BMI, age group, lifestyle risk, city tier, income and occupation
    to estimate which premium category you fall into.</p>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- form
CITIES_HINT = "e.g. Mumbai, Delhi, Bilaspur, Jaipur"
OCCUPATIONS = ["student", "teacher", "admin", "retired", "unemployed", "business_owner"]

st.markdown('<div class="section-title">Check your premium category</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">Fill in your details below. Height must be in metres.</div>',
    unsafe_allow_html=True,
)

with st.form("predict_form"):
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age", min_value=1, max_value=99, value=30, step=1)
        weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0, step=0.5)
    with c2:
        height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.70, step=0.01)
        income_lpa = st.number_input("Annual income (LPA)", min_value=0.1, value=10.0, step=0.5)
    with c3:
        city = st.text_input("City", value="Mumbai", help=CITIES_HINT)
        occupation = st.selectbox("Occupation", OCCUPATIONS, format_func=lambda x: x.replace("_", " ").title())
    smoker = st.checkbox("I am a smoker")
    submitted = st.form_submit_button("Predict premium")

# ---------------------------------------------------------------- result
if submitted:
    if not city.strip():
        st.warning("Please enter your city.")
    else:
        payload = {
            "age": int(age),
            "weight": float(weight),
            "height": float(height),
            "income_lpa": float(income_lpa),
            "smoker": bool(smoker),
            "city": city.strip().title(),
            "occupation": occupation,
        }
        try:
            with st.spinner("Calculating..."):
                resp = requests.post(API_URL, json=payload, timeout=15)
            if resp.status_code == 200:
                category = resp.json().get("predicted_category", "unknown")
                bmi = payload["weight"] / (payload["height"] ** 2)

                st.markdown(
                    f"""
<div class="result">
  <div class="label">Predicted premium category</div>
  <div class="value">{category}</div>
  <div class="note">Based on the details you provided. This is an estimate, not a final quote.</div>
</div>
""",
                    unsafe_allow_html=True,
                )

                m1, m2, m3 = st.columns(3)
                m1.markdown(
                    f'<div class="metric-card"><div class="m-val">{bmi:.1f}</div><div class="m-lab">Your BMI</div></div>',
                    unsafe_allow_html=True,
                )
                m2.markdown(
                    f'<div class="metric-card"><div class="m-val">{"Yes" if smoker else "No"}</div><div class="m-lab">Smoker</div></div>',
                    unsafe_allow_html=True,
                )
                m3.markdown(
                    f'<div class="metric-card"><div class="m-val">{payload["city"]}</div><div class="m-lab">City</div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.error(f"API error {resp.status_code}: {resp.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"Could not reach the API at {API_URL}. Is the FastAPI server running?")
        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again.")

# ---------------------------------------------------------------- stats strip
st.markdown(
    """
<div class="stats">
  <div class="card"><div class="num">90%</div><div class="lab">Prediction accuracy*</div></div>
  <div class="card"><div class="num">135+</div><div class="lab">Cities covered</div></div>
  <div class="card"><div class="num">3</div><div class="lab">City tiers modelled</div></div>
</div>
<div class="footer">*Illustrative figures. Replace with your model's real metrics.</div>
""",
    unsafe_allow_html=True,
)