import streamlit as st
import pandas as pd
from workflow import build_workflow

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="BiasGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>
/* Main App Background */
.stApp {
    background: linear-gradient(135deg, #0b1220 0%, #111827 45%, #172554 100%);
    color: white;
}

/* Remove Streamlit default spacing */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Header */
.hero-title {
    font-size: 54px;
    font-weight: 800;
    text-align: center;
    color: #60a5fa;
    margin-bottom: 0;
}

.hero-sub {
    text-align: center;
    color: #cbd5e1;
    font-size: 18px;
    margin-bottom: 28px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.25);
}

/* KPI cards */
.kpi {
    background: linear-gradient(135deg,#2563eb,#1d4ed8);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    color: white;
    font-weight: 700;
    box-shadow: 0 10px 22px rgba(37,99,235,0.35);
}

.kpi-label {
    font-size: 15px;
    color: #dbeafe;
}

.kpi-value {
    font-size: 28px;
    margin-top: 8px;
}

/* Verdict banners */
.good-box {
    background: linear-gradient(135deg,#14532d,#166534);
    border-radius: 18px;
    padding: 18px;
    color: white;
    font-weight: 700;
}

.warn-box {
    background: linear-gradient(135deg,#7f1d1d,#b91c1c);
    border-radius: 18px;
    padding: 18px;
    color: white;
    font-weight: 700;
}

/* Section title */
.section {
    font-size: 28px;
    font-weight: 800;
    margin-top: 14px;
    margin-bottom: 12px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HELPERS
# ---------------------------------------------------
def pct(x):
    try:
        return f"{round(float(x) * 100, 1)}%"
    except:
        return str(x)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.title("⚙️ BiasGuard AI")
    st.write("Audit decision datasets for hidden unfairness.")
    st.markdown("---")
    st.write("### Recommended Columns")
    st.caption("gender, age, selected, approved, hired")
    st.markdown("---")
    st.write("### Stack")
    st.caption("Streamlit • LangGraph • LangChain • Groq")

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown('<p class="hero-title">🛡️ BiasGuard AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-sub">Detect hidden unfairness in hiring, lending, admissions and AI decision systems.</p>',
    unsafe_allow_html=True
)

# ---------------------------------------------------
# UPLOAD SECTION
# ---------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
uploaded = st.file_uploader("📂 Upload CSV Dataset", type=["csv"])
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# EMPTY LANDING SCREEN
# ---------------------------------------------------
if not uploaded:
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h3>⚖️ Fairness Audit</h3>
        <p>Compare outcomes across demographic groups.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <h3>🧠 AI Insights</h3>
        <p>Explain patterns and generate recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        <h3>📄 Executive Reports</h3>
        <p>Ready-to-share decision governance summaries.</p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ---------------------------------------------------
# SAVE FILE
# ---------------------------------------------------
with open("temp.csv", "wb") as f:
    f.write(uploaded.read())

# ---------------------------------------------------
# RUN WORKFLOW
# ---------------------------------------------------
wf = build_workflow()

with st.spinner("🔍 Running fairness audit..."):
    result = wf.invoke({"file": "temp.csv"})

# ---------------------------------------------------
# ERROR
# ---------------------------------------------------
if "error" in result:
    st.error(result["error"])
    st.stop()

# ---------------------------------------------------
# READ VALUES
# ---------------------------------------------------
schema = result["schema"]
metrics = result["metrics"]

g1 = metrics["group1"]
g2 = metrics["group2"]
r1 = metrics["rate1"]
r2 = metrics["rate2"]
gap = metrics["gap"]
biased = metrics["biased"]

# ---------------------------------------------------
# VERDICT BANNER
# ---------------------------------------------------
st.markdown("##")

if biased:
    st.markdown(
        f"""
        <div class="warn-box">
        ⚠ HIGH RISK DISPARITY DETECTED<br><br>
        {g1.title()} selection rate: {pct(r1)}<br>
        {g2.title()} selection rate: {pct(r2)}<br>
        Outcome gap: {pct(gap)}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <div class="good-box">
        ✅ LOW RISK / FAIR OUTCOME PATTERN<br><br>
        Gap detected: {pct(gap)}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------
st.markdown('<div class="section">📊 Key Metrics</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">Sensitive Column</div><div class="kpi-value">{schema["sensitive"]}</div></div>',
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">Decision Column</div><div class="kpi-value">{schema["target"]}</div></div>',
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">Fairness Gap</div><div class="kpi-value">{pct(gap)}</div></div>',
        unsafe_allow_html=True
    )

with k4:
    risk = "High" if biased else "Low"
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">Risk Level</div><div class="kpi-value">{risk}</div></div>',
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# CHART + DETAILS
# ---------------------------------------------------
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="section">📈 Group Comparison</div>', unsafe_allow_html=True)

    chart_df = pd.DataFrame({
        "Group": [g1.title(), g2.title()],
        "Rate": [float(r1), float(r2)]
    })

    st.bar_chart(chart_df.set_index("Group"))

with right:
    st.markdown('<div class="section">🧾 Findings</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"**{g1.title()} Rate:** {pct(r1)}")
    st.write(f"**{g2.title()} Rate:** {pct(r2)}")
    st.write(f"**Gap:** {pct(gap)}")
    st.write(f"**Status:** {'Bias Risk Found' if biased else 'No Major Risk'}")
    st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------------------------------
# BIAS DRIVERS
# ---------------------------------------------------
st.markdown('<div class="section">🔍 Bias Drivers</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)

drivers = result.get("bias_diagnostics", [])

if drivers:
    for item in drivers:
        st.write("•", item)
else:
    st.write("No major bias drivers identified.")

st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------------------------------
# AI INSIGHT
# ---------------------------------------------------
st.markdown('<div class="section">🧠 AI Insight</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.write(result["summary"])
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------
st.markdown('<div class="section">🚀 Recommended Actions</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.write(result["recommendations"])
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# REPORT
# ---------------------------------------------------
st.markdown('<div class="section">📄 Executive Report</div>', unsafe_allow_html=True)

with st.expander("View Full Report"):
    st.text(result["report"])