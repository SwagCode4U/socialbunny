
router = APIRouter(prefix="/students", tags=["Students"])

# Menu (1,2,3...)
@router.get("/menu")
async def menu(db=Depends(get_db)):
    topics = await list_topics(db)
    return {i+1: t.title for i, t in enumerate(topics)}

# All Topics
@router.get("/topics")
async def topics(db=Depends(get_db)):
    return await list_topics(db)

# Topic Detail
@router.get("/topics/{id}")
async def topic(id: int, db=Depends(get_db)):
    return await topic_detail(db, id)

# Search
@router.get("/search")
async def search(q: str, db=Depends(get_db)):
    return await search_topic(db, q)

# Articles
@router.get("/articles/{topic_id}")
async def articles(topic_id: int, db=Depends(get_db)):
    return await topic_articles(db, topic_id)

# Quiz
@router.get("/quiz/{topic_id}")
async def quiz(topic_id: int, db=Depends(get_db)):
    return await topic_quiz(db, topic_id)


@router.get("/students")
def get_students():
    return {"msg":"list of students..."}


@router.get("/students/{id}")
def get_student(id: int):
    return {"msg": f"student with id {id}"}

@router.get("/study_corner")
def get_study_corner():
    return {"msg": "list of study corner topics..."}


from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.db import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    title = Column(String(100))
    content = Column(Text)


from sqlalchemy import Column, Integer, String, ForeignKey
from app.db import Base

class Quiz(Base):
    __tablename__ = "quiz"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    question = Column(String(255))
    option1 = Column(String(100))
    option2 = Column(String(100))
    option3 = Column(String(100))
    option4 = Column(String(100))
    answer = Column(String(100))


from sqlalchemy import column, Integer, String, Text
from app.db import base

class Study(base):
    __tablename__ = "study"

    id = column(Integer, primary_key=True, index=True)
    title = column(String, nullable=False)
    description = column(Text, nullable=True)




from sqlalchemy import Column, Integer, String, Text
from app.db import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    short_desc = Column(String(600))
    full_content = Column(Text)