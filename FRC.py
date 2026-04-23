import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.set_page_config(page_title="ChimeK Analyzer Pro", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.hero {
    padding: 30px;
    border-radius: 15px;
    background: linear-gradient(135deg, #6fb1fc, #4364f7);
    color: white;
    text-align:center;
}
.card {
    padding: 20px;
    border-radius: 12px;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class='hero'>
<h1>🔔 ChimeK Financial Health Analyzer</h1>
<p>Turn financial data into decisions in seconds ✨</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUT MODE ----------------
mode = st.radio("📌 Choose Input Method:", ["📂 Upload Excel", "✍️ Manual Entry"])

def safe_div(a, b):
    return a / b if b != 0 else 0

data = {}

# ---------------- INPUT ----------------
if mode == "📂 Upload Excel":
    file = st.file_uploader("📤 Upload Excel File", type=["xlsx"])
    if file:
        df = pd.read_excel(file)
        data = df.iloc[0].to_dict()
        st.success("✅ File uploaded successfully!")
    else:
        st.info("Upload a file or switch to manual entry ✍️")

else:
    st.subheader("✍️ Enter Financial Data")

    col1, col2 = st.columns(2)

    with col1:
        data["Revenue"] = st.number_input("💰 Revenue", 100000.0)
        data["Profit"] = st.number_input("📈 Net Profit", 10000.0)
        data["Current Assets"] = st.number_input("🏦 Current Assets", 50000.0)
        data["Current Liabilities"] = st.number_input("📉 Current Liabilities", 25000.0)

    with col2:
        data["Debt"] = st.number_input("⚖️ Debt", 40000.0)
        data["Equity"] = st.number_input("📊 Equity", 60000.0)

# ---------------- PROCESS ----------------
if data:

    revenue = data.get("Revenue", 0)
    profit = data.get("Profit", 0)
    ca = data.get("Current Assets", 0)
    cl = data.get("Current Liabilities", 0)
    debt = data.get("Debt", 0)
    equity = data.get("Equity", 0)

    # Core Ratios
    current_ratio = safe_div(ca, cl)
    profit_margin = safe_div(profit, revenue)
    de_ratio = safe_div(debt, equity)

    # ---------------- SCORE ----------------
    score = 0
    if current_ratio > 1.5: score += 30
    elif current_ratio > 1: score += 15

    if profit_margin > 0.1: score += 30
    elif profit_margin > 0.05: score += 15

    if de_ratio < 1: score += 40
    elif de_ratio < 2: score += 20

    # ---------------- DASHBOARD ----------------
    st.write("## 📊 Financial Snapshot")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card'><h3>💯 Health Score</h3><h1>{score}</h1></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h3>💰 Profitability</h3><h1>{profit_margin:.2f}</h1></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><h3>⚖️ Risk Level</h3><h1>{de_ratio:.2f}</h1></div>", unsafe_allow_html=True)

    st.progress(score)

    # ---------------- MOOD ----------------
    if score > 70:
        mood = "😎 Strong & Investor Friendly"
    elif score > 40:
        mood = "🙂 Stable"
    else:
        mood = "😬 Risky"

    st.write(f"### 📌 Company Status: {mood}")

    # ---------------- RADAR CHART ----------------
    st.subheader("📊 Performance Overview")

    liquidity_score = min(current_ratio * 40, 100)
    profitability_score = min(profit_margin * 500, 100)
    leverage_score = 100 - min(de_ratio * 40, 100)
    efficiency_score = 60
    market_score = 50

    categories = ["Liquidity", "Profitability", "Leverage", "Efficiency", "Market"]
    scores = [liquidity_score, profitability_score, leverage_score, efficiency_score, market_score]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=categories,
        fill='toself'
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- INSIGHT CARDS ----------------
    st.subheader("🤖 AI Insights Summary")

    col1, col2, col3 = st.columns(3)

    # Strengths
    strengths = []
    if current_ratio > 1.5:
        strengths.append("Strong liquidity position")
    if profit_margin > 0.1:
        strengths.append("Healthy profitability")
    if de_ratio < 1:
        strengths.append("Low financial risk")

    with col1:
        st.markdown("### ✅ Strengths")
        if strengths:
            for s in strengths:
                st.success(s)
        else:
            st.info("No major strengths")

    # Risks
    risks = []
    if current_ratio < 1:
        risks.append("Liquidity risk")
    if de_ratio > 2:
        risks.append("High leverage risk")
    if profit_margin < 0.05:
        risks.append("Low profitability")

    with col2:
        st.markdown("### ⚠️ Watchouts")
        if risks:
            for r in risks:
                st.warning(r)
        else:
            st.success("No major risks")

    # Suggestions
    suggestions = []
    if current_ratio < 1:
        suggestions.append("Improve short-term asset management")
    if de_ratio > 2:
        suggestions.append("Reduce debt dependency")
    if profit_margin < 0.05:
        suggestions.append("Improve cost efficiency")

    with col3:
        st.markdown("### 💡 Suggestions")
        if suggestions:
            for s in suggestions:
                st.info(s)
        else:
            st.success("Operations look optimized")

    # ---------------- SUMMARY ----------------
    summary = f"""
Financial Health Score: {score}
Company Status: {mood}

Liquidity: {'Strong' if current_ratio>1 else 'Weak'}
Profitability: {'Healthy' if profit_margin>0.1 else 'Moderate'}
Leverage: {'Controlled' if de_ratio<2 else 'High Risk'}
"""

    st.subheader("🧾 Executive Summary")
    st.success(summary)

    # ---------------- PDF ----------------
    def create_pdf(text):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        doc = SimpleDocTemplate(temp_file.name)
        styles = getSampleStyleSheet()

        content = []
        for line in text.split("\n"):
            content.append(Paragraph(line, styles["Normal"]))
            content.append(Spacer(1, 10))

        doc.build(content)
        return temp_file.name

    pdf_file = create_pdf(summary)

    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download PDF Report", f, file_name="Financial_Report.pdf")