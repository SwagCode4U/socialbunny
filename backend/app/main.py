import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app.database import get_db
from app.models import User, UserRole
from app.routes import project_routes, admin_routes, news_routes, topic_routes, auth_routes, referral_routes

load_dotenv()

app = FastAPI(title="SocialBunny API", version="1.0")

# CORS — allow frontend on any origin during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to SocialBunny API"}


# Public referral landing: /login/ha8080k  → redirects to frontend
@app.get("/login/{ref_code}")
def referral_landing(ref_code: str, db: Session = Depends(get_db)):
    admin = db.query(User).filter(
        User.referral_code == ref_code,
        User.role == UserRole.admin,
    ).first()
    if not admin:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Invalid referral link")
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return RedirectResponse(url=f"{FRONTEND_URL}/register?ref={ref_code}")


# Register routers
app.include_router(project_routes.router)
app.include_router(admin_routes.router)
app.include_router(news_routes.router)
app.include_router(topic_routes.router)
app.include_router(auth_routes.router)
app.include_router(referral_routes.router)
