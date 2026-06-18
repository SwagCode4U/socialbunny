from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Topic
from app.schemas import TopicCreate, TopicDetail, TopicListResponse
router = APIRouter(prefix="/api/topics", tags=["topics"])
def make_preview(topic: Topic) -> dict:
    lines = topic.content.split("\n")
    preview_lines = lines[:30]
    return {
        "id": topic.id,
        "title": topic.title,
        "author": topic.author,
        "created_at": topic.created_at,
        "preview": "\n".join(preview_lines),
    }
@router.post("/", response_model=TopicDetail)
def create_topic(body: TopicCreate, db: Session = Depends(get_db)):
    topic = Topic(
        title=body.title,
        content=body.content,
        author=body.author,
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic
@router.get("/", response_model=TopicListResponse)
def list_topics(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    total = db.query(Topic).count()
    topics = (
        db.query(Topic)
        .order_by(Topic.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "topics": [make_preview(t) for t in topics],
    }
@router.get("/{topic_id}", response_model=TopicDetail)
def get_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic