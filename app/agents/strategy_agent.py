from app.services.llm_services import get_llm
import json


# -----------------------------
#  IMPROVED CONFIDENCE LOGIC
# -----------------------------
def calculate_confidence(news, financial_data, analysis):
    score = 0

    # ---------------- NEWS QUALITY ----------------
    if news and "No recent" not in str(news):
        score += min(len(news) * 5, 30)

    # ---------------- FINANCIAL DATA QUALITY ----------------
    valid_fields = [v for v in financial_data.values() if v not in [None, 0, "N/A"]]
    score += min(len(valid_fields) * 8, 40)

    # ---------------- ANALYSIS QUALITY ----------------
    if analysis.get("summary") not in ["", "N/A"]:
        score += 10

    if analysis.get("key_risks"):
        score += 10

    if analysis.get("opportunities"):
        score += 10

    return min(score, 100)


# -----------------------------
# STRATEGY AGENT
# -----------------------------
def strategy_agent(state):

    llm = get_llm()

    company = state.get("company", "unknown")
    analysis = state.get("analysis", {})
    news = state.get("news", [])
    financial_data = state.get("financial_data", {})

    #  Updated confidence
    confidence_score = calculate_confidence(news, financial_data, analysis)

    if confidence_score >= 75:
        confidence_label = "High"
    elif confidence_score >= 50:
        confidence_label = "Medium"
    else:
        confidence_label = "Low"

    # -----------------------------
    # Load prompt
    # -----------------------------
    with open("app/prompts/strategy_prompt.txt") as f:
        template = f.read()

    prompt = template.format(
        company=company,
        analysis=json.dumps(analysis, indent=2),
        confidence=confidence_label
    )

    # -----------------------------
    # LLM CALL + SAFE JSON PARSING
    # -----------------------------
    try:
        response = llm.invoke(prompt)
        raw_output = response.content if isinstance(response.content, str) else str(response.content)

        try:
            parsed_output = json.loads(raw_output)

            # Handle double-encoded JSON
            if isinstance(parsed_output, str):
                parsed_output = json.loads(parsed_output)

        except Exception as e:
            print("⚠️ Strategy JSON parsing failed:", str(e))
            parsed_output = {}

    except Exception as e:
        parsed_output = {
            "decision": "Hold",
            "reason": f"LLM error: {str(e)}",
            "risks": [],
            "opportunities": []
        }

    # -----------------------------
    # Ensure required keys
    # -----------------------------
    if not isinstance(parsed_output, dict):
        parsed_output = {}

    parsed_output.setdefault("decision", "Hold")
    parsed_output.setdefault("reason", "No reasoning provided")
    parsed_output.setdefault("risks", [])
    parsed_output.setdefault("opportunities", [])

    # -----------------------------
    # FINAL STRUCTURED OUTPUT
    # -----------------------------
    state["strategy"] = {
        "decision": parsed_output["decision"],
        "reason": parsed_output["reason"],
        "risks": parsed_output["risks"],
        "opportunities": parsed_output["opportunities"],
        "confidence_score": confidence_score,
        "confidence_label": confidence_label
    }

    return state