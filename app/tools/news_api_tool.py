import requests
from app.config.settings import settings

def fetch_news(company: str):
    try:
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": f"{company} stock OR {company} earnings OR {company} business",
            "apiKey": settings.NEWS_API_KEY,
            "pageSize": 5,
            "sortBy": "publishedAt",
            "language": "en"
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            return {"error": f"News API failed with status {response.status_code}"}

        data = response.json()

        if data.get("status") != "ok":
            return {"error": data}

        articles = []

        for article in data.get("articles", []):
            title = article.get("title", "").lower()

            if company.lower() not in title:
                continue

            articles.append({
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "url": article.get("url"),
                "published_at": article.get("publishedAt")
            })

        return articles[:5]

    except Exception as e:
        return {"error": str(e)}