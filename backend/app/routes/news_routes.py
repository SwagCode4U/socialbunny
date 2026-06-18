from fastapi import APIRouter, Query
from app.schemas import NewsResponse
from app.news_fetcher import fetch_news

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/", response_model=NewsResponse)
def list_news(
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        10, ge=1, le=50, description="Max items per page (default 10, max 50)"
    ),
):
    return fetch_news(offset=offset, limit=limit)
