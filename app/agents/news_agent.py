from app.tools.news_api_tool import fetch_news

def news_agent(state):

    company = state["company"]

    news = fetch_news(company)

    return {
        "news": news
    }
