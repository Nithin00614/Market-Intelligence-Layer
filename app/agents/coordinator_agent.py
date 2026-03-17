from app.services.llm_services import get_llm

def coordinator_agent(state):

    llm = get_llm()

    company = state["company"]

    prompt = f"""
You are a market intelligence coordinator.

Your job is to decide which tools should be used to analyze the company.

Company: {company}

Available tools:
1. news_agent → fetch latest company news
2. financial_agent → fetch financial metrics

Return the tools needed in order.

Example:
news_agent, financial_agent
"""

    response = llm.invoke(prompt)

    decision = response.content.lower()

    return {
        "tool_plan": decision
    }