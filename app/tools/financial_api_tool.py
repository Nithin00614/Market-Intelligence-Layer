import yfinance as yf

def fetch_financial_data(company: str):
    try:
        ticker_map = {
            "apple": "AAPL",
            "tesla": "TSLA",
            "amazon": "AMZN",
            "google": "GOOGL",
            "nvidia": "NVDA"
        }


        ticker = ticker_map.get(company.lower(), company)

        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "company": ticker,
            "price": info.get("currentPrice") or "N/A",
            "market_cap": info.get("marketCap") or "N/A",
            "pe_ratio": info.get("trailingPE") or "N/A",
            "revenue_growth": info.get("revenueGrowth") or "N/A",
            "profit_margin": info.get("profitMargins") or "N/A"
        }

    except Exception as e:
        return {"error": str(e)}