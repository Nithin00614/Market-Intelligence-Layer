import streamlit as st
import requests
import time

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Market Intelligence",
    layout="wide",
    page_icon="📊"
)

# -------------------------------
# CUSTOM CSS (UI POLISH)
# -------------------------------
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.center {
    text-align: center;
}

.card {
    background-color: #161A23;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
}

[data-testid="metric-container"] {
    background-color: #161A23;
    border-radius: 10px;
    padding: 12px;
}

.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 8px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown(
    "<h1 class='center' style='margin-bottom:0;'>📊 AI Market Intelligence System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='center' style='color:gray;margin-top:5px;'>Multi-Agent RAG powered market insights</p>",
    unsafe_allow_html=True
)

st.write("")

# -------------------------------
# INPUT SECTION
# -------------------------------
col1, col2 = st.columns([4, 1], vertical_alignment="bottom")

with col1:
    company = st.selectbox(
        "Select Company",
        ["Apple", "Tesla", "Amazon", "Google", "Nvidia"]
    )

with col2:
    analyze_btn = st.button("🚀 Analyze")

# -------------------------------
# ANALYSIS CALL
# -------------------------------
if analyze_btn:

    start_time = time.time()

    with st.spinner("Analyzing market data..."):

        response = requests.post(
            "http://127.0.0.1:8000/api/analyze-market",
            json={
                "company": company,
                "question": f"Analyze {company}'s market position"
            }
        )

        data = response.json()

    end_time = time.time()

    st.success(f"✅ Analysis completed in {round(end_time - start_time, 2)}s")

    # -------------------------------
    # FINANCIAL OVERVIEW
    # -------------------------------
    financial = data.get("financial_data", {})

    if financial:
        st.markdown("## 📊 Financial Overview")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Price", financial.get("price", "N/A"))
        c2.metric("Market Cap", f"{round(financial.get('market_cap', 0)/1e12,2)}T")
        c3.metric("Revenue Growth", f"{round(financial.get('revenue_growth', 0)*100,2)}%")
        c4.metric("Profit Margin", f"{round(financial.get('profit_margin', 0)*100,2)}%")

        # Chart
        st.bar_chart({
            "Profit Margin": financial.get("profit_margin", 0),
            "Revenue Growth": financial.get("revenue_growth", 0)
        })

    # -------------------------------
    # ANALYSIS
    # -------------------------------
    analysis = data.get("analysis", {})

    if analysis:
        st.markdown("## 📈 Market Analysis")

        st.markdown(
            f"<div class='card' style='font-size:16px;line-height:1.6'>{analysis.get('summary','N/A')}</div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        # RISKS
        with col1:
            st.markdown("### ⚠️ Risks")
            risks = analysis.get("key_risks", [])

            if risks:
                for r in risks:
                    st.markdown(f"- {r}")
            else:
                st.write("No major risks identified")

        # OPPORTUNITIES
        with col2:
            st.markdown("### 🚀 Opportunities")
            opps = analysis.get("opportunities", [])

            if opps:
                for o in opps:
                    st.markdown(f"- {o}")
            else:
                st.write("No major opportunities identified")

        # SOURCES
        with st.expander("📚 Sources & Citations"):
            citations = analysis.get("citations", [])

            if citations:
                for c in citations:
                    st.markdown(f"**[{c['id']}] {c['source']}**")
                    st.caption(c.get("snippet", ""))
            else:
                st.write("No sources available")

    # -------------------------------
    # STRATEGY
    # -------------------------------
    strategy = data.get("strategy", {})

    if strategy:
        st.markdown("## 📊 Investment Strategy")

        c1, c2, c3 = st.columns(3)

        c1.metric("Decision", strategy.get("decision", "N/A"))
        c2.metric("Confidence", strategy.get("confidence_label", "N/A"))
        c3.metric("Score", strategy.get("confidence_score", "N/A"))

        st.markdown(
            f"<div class='card'>{strategy.get('reason','N/A')}</div>",
            unsafe_allow_html=True
        )