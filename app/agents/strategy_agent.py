from app.services.llm_services import get_llm

def strategy_agent(state):

    llm = get_llm()

    company = state["company"]
    analysis = state["analysis"]

    # load prompt template
    with open("app/prompts/strategy_prompt.txt") as f:
        template = f.read()

    prompt = template.format(
        company=company,
        analysis=analysis
    )

    response = llm.invoke(prompt)

    return {
        "final_report": response.content
    }