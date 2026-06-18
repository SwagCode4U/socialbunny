from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from app.database import get_db
from app.models import User, UserRole
from app.schemas import (
    GoogleAuthRequest,
    GoogleAuthResponse,
    UserResponse,
    WizardUpdate,
)
from app.utils import create_access_token, verify_access_token
import os

router = APIRouter(prefix="/api/auth", tags=["auth"])
security = HTTPBearer()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


@router.post("/google", response_model=GoogleAuthResponse)
def google_login(body: GoogleAuthRequest, db: Session = Depends(get_db)):
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="GOOGLE_CLIENT_ID not configured")

    try:
        info = id_token.verify_oauth2_token(
            body.id_token, requests.Request(), GOOGLE_CLIENT_ID
        )
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")

    google_sub = info["sub"]
    email = info.get("email", "")
    name = info.get("name", "")
    picture = info.get("picture", "")

    user = db.query(User).filter(
        (User.google_sub == google_sub) | (User.email == email)
    ).first()

    if user:
        user.name = name
        user.picture = picture
        if not user.google_sub:
            user.google_sub = google_sub
        db.commit()
        db.refresh(user)
    else:
        user = User(
            google_sub=google_sub,
            email=email,
            name=name,
            picture=picture,
            role=UserRole.student,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token_data = create_access_token(user.id)

    return {
        "access_token": token_data["access_token"],
        "token_type": token_data["token_type"],
        "expires_in": token_data["expires_in"],
        "user": user,
    }


@router.post("/wizard", response_model=UserResponse)
def complete_wizard(
    body: WizardUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    user_id = verify_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = body.name
    user.phone = body.phone
    user.interest = body.interest
    if body.referred_by_id:
        referrer = db.query(User).filter(User.id == body.referred_by_id).first()
        if not referrer or referrer.role != UserRole.admin:
            raise HTTPException(status_code=400, detail="Invalid referral")
        user.referred_by_id = body.referred_by_id

    db.commit()
    db.refresh(user)
    return user
