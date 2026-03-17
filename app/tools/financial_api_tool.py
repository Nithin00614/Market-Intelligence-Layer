import requests
from app.config.settings import settings

def fetch_financial_data(company):

    url = f"https://financialmodelingprep.com/api/v3/profile/{company}?apikey={settings.FINANCIAL_API_KEY}"

    response = requests.get(url)

    data = response.json()

    # Handle error responses or empty lists
    if isinstance(data, dict) and "error" in data:
        return {"error": data.get("error", "Unknown error")}
    
    if not isinstance(data, list) or len(data) == 0:
        return {}

    profile = data[0]

    # Safely extract fields with defaults
    return {
        "company": profile.get("companyName", "N/A"),
        "price": profile.get("price", 0),
        "market_cap": profile.get("mktCap", "N/A"),
        "sector": profile.get("sector", "N/A")
    }

