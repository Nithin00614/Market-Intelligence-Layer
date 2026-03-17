from app.tools.financial_api_tool import fetch_financial_data

def financial_data_agent(state):

    company = state["company"]

    financial_data = fetch_financial_data(company)

    return {
        "financial_data": financial_data
    }
