import streamlit as st
import requests

st.title("📊 AI Market Intelligence System")

company = st.selectbox(
    "Select Company",
    ["Apple", "Tesla", "Amazon", "Google", "Nvidia"]
)

if st.button("Analyze"):

    response = requests.post(
        "http://127.0.0.1:8000/api/analyze-market",
        json={"company": company, "question": f"Analyze {company}'s market position"}
    )

    data = response.json()

    if "analysis" in data:
        st.subheader("📈 Analysis")
        st.write(data["analysis"].get("summary", "N/A"))

        st.subheader("⚠️ Risks")
        st.write(data["analysis"].get("key_risks", []))

        st.subheader("🚀 Opportunities")
        st.write(data["analysis"].get("opportunities", []))

    if "strategy" in data:
        st.subheader("📊 Strategy")
        st.write(data["strategy"].get("decision", "N/A"))
        st.write(data["strategy"].get("reason", "N/A"))

        st.subheader("🔍 Confidence")
        st.write(data["strategy"].get("confidence_label", "N/A"))