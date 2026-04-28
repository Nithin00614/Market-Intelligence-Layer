from app.tools.financial_api_tool import fetch_financial_data

COMPANY_SYMBOL_MAP = {
        "apple": "AAPL",
        "tesla": "TSLA",
        "google": "GOOGL",
        "microsoft": "MSFT",
    }

def financial_data_agent(state):

    company_name = state.get("company", "").lower().strip()
    company = COMPANY_SYMBOL_MAP.get(company_name, company_name.upper())

    try:
        financial_data = fetch_financial_data(company)
    except Exception as e:
        financial_data = {"error": str(e)}

    state["financial_data"] = financial_data or {}
    return state
