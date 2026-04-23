import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

st.set_page_config(page_title="FinHealth Analyzer", layout="wide")

# ---------- STYLE ----------
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

# ---------- HEADER ----------
st.markdown("""
<div class='hero'>
<h1>🔔 FinHealth Analyzer</h1>
<p>Turn financial data into decisions in seconds ✨</p>
</div>
""", unsafe_allow_html=True)

# ---------- FUNCTIONS ----------
def safe_div(a, b):
    try:
        return a / b if b != 0 else 0
    except:
        return 0

def status(val, good, moderate):
    if val >= good:
        return "🟢 Strong"
    elif val >= moderate:
        return "🟡 Moderate"
    else:
        return "🔴 Weak"

# ---------- INPUT ----------
mode = st.radio("📌 Choose Input Method:", ["📂 Upload Excel", "✍️ Manual Entry"])

data = {}

if mode == "📂 Upload Excel":
    file = st.file_uploader("📤 Upload Excel File", type=["xlsx"])
    if file:
        df = pd.read_excel(file)
        data = df.iloc[0].to_dict()
        st.success("✅ File uploaded successfully!")
    else:
        st.info("Upload file or switch to manual entry ✍️")

else:
    st.subheader("✍️ Enter Financial Data")

    col1, col2 = st.columns(2)

    with col1:
        data["Revenue"] = st.number_input("💰 Revenue", value=100000.0)
        data["Profit"] = st.number_input("📈 Net Profit", value=10000.0)
        data["Current Assets"] = st.number_input("🏦 Current Assets", value=50000.0)
        data["Current Liabilities"] = st.number_input("📉 Current Liabilities", value=25000.0)

    with col2:
        data["Debt"] = st.number_input("⚖️ Debt", value=40000.0)
        data["Equity"] = st.number_input("📊 Equity", value=60000.0)
        data["Inventory"] = st.number_input("📦 Inventory", value=10000.0)
        data["Total Assets"] = st.number_input("🏢 Total Assets", value=120000.0)

# ---------- PROCESS ----------
if data:

    revenue = data.get("Revenue", 0)
    profit = data.get("Profit", 0)
    ca = data.get("Current Assets", 0)
    cl = data.get("Current Liabilities", 0)
    debt = data.get("Debt", 0)
    equity = data.get("Equity", 0)
    inventory = data.get("Inventory", 0)
    assets = data.get("Total Assets", 1)

    # ---------- RATIOS ----------
    current_ratio = safe_div(ca, cl)
    quick_ratio = safe_div(ca - inventory, cl)
    profit_margin = safe_div(profit, revenue)
    roe = safe_div(profit, equity)
    de_ratio = safe_div(debt, equity)
    debt_ratio = safe_div(debt, assets)

    # ---------- SCORE ----------
    score = 0
    if current_ratio > 1.5: score += 30
    elif current_ratio > 1: score += 15

    if profit_margin > 0.1: score += 30
    elif profit_margin > 0.05: score += 15

    if de_ratio < 1: score += 40
    elif de_ratio < 2: score += 20

    # ---------- DASHBOARD ----------
    st.write("## 📊 Financial Snapshot")

    c1, c2, c3 = st.columns(3)

    c1.markdown(f"<div class='card'><h3>💯 Health Score</h3><h1>{score}</h1></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='card'><h3>💰 Profitability</h3><h1>{profit_margin:.2f}</h1></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='card'><h3>⚖️ Risk</h3><h1>{de_ratio:.2f}</h1></div>", unsafe_allow_html=True)

    st.progress(score)

    # ---------- STATUS ----------
    if score > 70:
        mood = "😎 Strong"
    elif score > 40:
        mood = "🙂 Moderate"
    else:
        mood = "😬 Risky"

    st.write(f"### 📌 Company Status: {mood}")

    # ---------- RADAR ----------
    st.subheader("📊 Performance Overview")

    categories = ["Liquidity", "Profitability", "Leverage", "Efficiency", "Market"]
    scores = [
        min(current_ratio * 40, 100),
        min(profit_margin * 500, 100),
        100 - min(de_ratio * 40, 100),
        60,
        50
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=scores, theta=categories, fill='toself'))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100])))
    st.plotly_chart(fig, use_container_width=True)

    # ---------- INSIGHTS ----------
    st.subheader("🤖 Insights")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### ✅ Strengths")
        if current_ratio > 1.5:
            st.success("Strong liquidity")
        if profit_margin > 0.1:
            st.success("Healthy profitability")
        if de_ratio < 1:
            st.success("Low financial risk")

    with col2:
        st.markdown("### ⚠️ Risks")
        if current_ratio < 1:
            st.warning("Liquidity issue")
        if de_ratio > 2:
            st.warning("High debt")
        if profit_margin < 0.05:
            st.warning("Low profitability")

    with col3:
        st.markdown("### 💡 Suggestions")
        if current_ratio < 1:
            st.info("Improve short-term assets")
        if de_ratio > 2:
            st.info("Reduce debt")
        if profit_margin < 0.05:
            st.info("Control costs")

    # ---------- EXPANDABLE RATIOS ----------
    st.subheader("📂 Detailed Analysis")

    with st.expander("💧 Liquidity"):
        st.write(f"Current Ratio = CA / CL → {current_ratio:.2f} ({status(current_ratio,1.5,1)})")
        st.write(f"Quick Ratio = (CA - Inventory) / CL → {quick_ratio:.2f} ({status(quick_ratio,1,0.5)})")

    with st.expander("💰 Profitability"):
        st.write(f"Profit Margin = Profit / Revenue → {profit_margin:.2f} ({status(profit_margin,0.1,0.05)})")
        st.write(f"ROE = Profit / Equity → {roe:.2f} ({status(roe,0.15,0.08)})")

    with st.expander("⚖️ Leverage"):
        st.write(f"Debt/Equity → {de_ratio:.2f}")
        st.write(f"Debt Ratio → {debt_ratio:.2f}")

    # ---------- SUMMARY ----------
    summary = f"""
Financial Health Score: {score}
Status: {mood}
Liquidity: {'Strong' if current_ratio>1 else 'Weak'}
Profitability: {'Healthy' if profit_margin>0.1 else 'Moderate'}
Leverage: {'Controlled' if de_ratio<2 else 'High'}
"""

    st.subheader("🧾 Summary")
    st.success(summary)

    # ---------- PDF ----------
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf():
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(file.name)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("ChimeK Financial Report", styles["Title"]))
    content.append(Spacer(1,20))

    content.append(Paragraph(f"Health Score: {score}", styles["Normal"]))
    content.append(Paragraph(f"Status: {mood}", styles["Normal"]))
    content.append(Spacer(1,10))

    content.append(Paragraph("Key Ratios:", styles["Heading2"]))
    content.append(Paragraph(f"Current Ratio: {current_ratio:.2f}", styles["Normal"]))
    content.append(Paragraph(f"Profit Margin: {profit_margin:.2f}", styles["Normal"]))
    content.append(Paragraph(f"Debt/Equity: {de_ratio:.2f}", styles["Normal"]))
    content.append(Spacer(1,10))

    content.append(Paragraph("Insights:", styles["Heading2"]))

    for i in insights:
        content.append(Paragraph(f"- {i}", styles["Normal"]))

    doc.build(content)
    return file.name
    pdf = create_pdf(summary)
        with open(pdf, "rb") as f:
           st.download_button("📄 Download PDF", f, file_name="report.pdf")
