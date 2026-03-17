from app.services.llm_services import get_llm
from app.tools.vector_retrieval_tool import retrieve_market_knowledge

def analysis_agent(state):

    llm = get_llm()

    company = state["company"]
    news = state.get("news", [])
    financial_data = state.get("financial_data", {})
    knowledge = retrieve_market_knowledge(company)

    with open("app/prompts/analysis_prompt.txt") as f:
        template = f.read()

    prompt = template.format(
    company=company,
    news=news,
    financial_data=financial_data,
    knowledge=knowledge
)

    response = llm.invoke(prompt)

    return {"analysis": response.content}