import requests
from app.config.settings import settings

def fetch_news(company):

    url = f"https://newsapi.org/v2/everything?q={company}&apiKey={settings.NEWS_API_KEY}"

    response = requests.get(url)

    data = response.json()

    # Handle error responses
    if not data.get("articles"):
        return []

    articles = []

    for article in data["articles"][:5]:
        title = article.get("title", "No title")
        articles.append(title)

    return articles
