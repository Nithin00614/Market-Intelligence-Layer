from app.tools.news_api_tool import fetch_news
from datetime import datetime, timedelta

# Trusted sources with credibility scores
TRUSTED_SOURCES = {
    "reuters": 0.95,
    "bloomberg": 0.95,
    "cnbc": 0.9,
    "wall street journal": 0.92,
    "financial times": 0.92,
    "yahoo finance": 0.85,
}


def get_credibility(source: str) -> float:
    if not source:
        return 0.6
    return TRUSTED_SOURCES.get(source.lower(), 0.6)


def is_recent(published_at: str, days: int = 7) -> bool:
    try:
        article_date = datetime.fromisoformat(published_at.replace("Z", ""))
        return article_date >= datetime.now() - timedelta(days=days)
    except:
        return True


def news_agent(state):
    company = state["company"]
    raw_news = fetch_news(company)
    processed_news = []

    for article in raw_news:
        # Safety fallback (handles unexpected formats)
        if not isinstance(article, dict):
            article = {
                "title": str(article),
                "source": "unknown",
                "url": "",
                "published_at": ""
            }

        source = article.get("source", "unknown")
        published_at = article.get("published_at", "")

        credibility = get_credibility(source)

        enriched_article = {
            "title": article.get("title", "No title"),
            "source": source,
            "url": article.get("url", ""),
            "published_at": published_at,
            "credibility_score": credibility,
        }

        processed_news.append(enriched_article)

    # Filter: credible + recent
    filtered_news = processed_news
    if not filtered_news:
        filtered_news = [
    "No recent high-impact financial news available"
]


    state["news"] = filtered_news 
    return state