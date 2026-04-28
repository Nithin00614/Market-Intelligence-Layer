import json
from app.services.llm_services import get_llm


def analysis_agent(state):
    llm = get_llm()

    # -----------------------------
    # Extract inputs
    # -----------------------------
    company = state.get("company", "")
    all_news = state.get("news", [])
    financial_data = state.get("financial_data", {})

    # -----------------------------
    # RAG knowledge from graph
    # -----------------------------
    retrieved_docs = state.get("knowledge", [])

    #  FIX: remove duplicate documents
    seen = set()
    filtered_docs = []

    for doc in retrieved_docs:
        text = doc.get("text", "")
        if text not in seen:
            seen.add(text)
            filtered_docs.append(doc)

    retrieved_docs = filtered_docs

    # -----------------------------
    # Format RAG knowledge + citations
    # -----------------------------
    knowledge_text_list = []
    citations = []

    for i, doc in enumerate(retrieved_docs):
        text = doc.get("text", "")
        source = doc.get("source", "unknown")

        knowledge_text_list.append(f"[{i+1}] {text}")

        citations.append({
            "id": i + 1,
            "source": source,
            "snippet": text[:120]
        })

    knowledge_text = "\n".join(knowledge_text_list)

    # -----------------------------
    # News formatting
    # -----------------------------
    formatted_news_list = []

    for n in all_news[:5]:
        if isinstance(n, dict):
            title = n.get("title", "No title")
            source = n.get("source", "unknown")
        else:
            title = str(n)
            source = "unknown"

        formatted_news_list.append(f"- {title} ({source})")

    formatted_news = "\n".join(formatted_news_list)

    # -----------------------------
    # Load prompt
    # -----------------------------
    with open("app/prompts/analysis_prompt.txt") as f:
        template = f.read()

    prompt = template.format(
        company=company,
        news=formatted_news,
        financial_data=json.dumps(financial_data, indent=2),
        knowledge=knowledge_text
    )

    # -----------------------------
    # LLM CALL
    # -----------------------------
    response = llm.invoke(prompt)
    raw_output = response.content if isinstance(response.content, str) else str(response.content)

    # -----------------------------
    # SAFE JSON PARSING
    # -----------------------------
    try:
        parsed_output = json.loads(raw_output)

        # Handle double-encoded JSON
        if isinstance(parsed_output, str):
            parsed_output = json.loads(parsed_output)

    except Exception as e:
        print("⚠️ JSON parsing failed:", str(e))
        parsed_output = {}

    if not isinstance(parsed_output, dict):
        parsed_output = {}

    # -----------------------------
    #  STRONG FALLBACK HANDLING
    # -----------------------------
    required_keys = ["summary", "sentiment", "key_risks", "opportunities"]

    for key in required_keys:
        if key not in parsed_output or parsed_output[key] in ["", "N/A", None, []]:

            if key == "summary":
                parsed_output[key] = (
                    f"{company} shows revenue growth of {financial_data.get('revenue_growth', 'N/A')} "
                    f"and profit margin of {financial_data.get('profit_margin', 'N/A')}, "
                    "indicating moderate growth with profitability considerations."
                )

            elif key == "sentiment":
                parsed_output[key] = "neutral"

            elif key == "key_risks":
                parsed_output[key] = ["No clear risks identified"]

            elif key == "opportunities":
                parsed_output[key] = ["No clear opportunities identified"]

    # -----------------------------
    # Attach citations
    # -----------------------------
    parsed_output["citations"] = citations

    # -----------------------------
    # Return
    # -----------------------------
    state["analysis"] = parsed_output
    return state