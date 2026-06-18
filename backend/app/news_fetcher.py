# app/news_fetcher.py

import feedparser
from datetime import datetime

RSS_URL = "https://news.yahoo.com/rss/india"


def fetch_news(offset: int = 0, limit: int = 10) -> dict:
    feed = feedparser.parse(RSS_URL)

    entries = []
    for entry in feed.entries:
        published_dt = None
        if "published_parsed" in entry and entry.published_parsed:
            published_dt = datetime(*entry.published_parsed[:6])

        entries.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "summary": entry.get("summary", "")[:200],
            "published": entry.get("published", ""),
            "published_parsed": published_dt.isoformat() if published_dt else None,
        })

    entries.sort(key=lambda e: e["published_parsed"] or "", reverse=True)

    total = len(entries)
    paginated = entries[offset: offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": paginated,
    }
