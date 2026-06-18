import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.schemas import ReferralLookupResponse

router = APIRouter(prefix="/api/referral", tags=["referral"])


@router.get("/lookup/{code}", response_model=ReferralLookupResponse)
def lookup_referral(code: str, db: Session = Depends(get_db)):
    admin = db.query(User).filter(
        User.referral_code == code,
        User.role == UserRole.admin,
    ).first()

    if not admin:
        raise HTTPException(status_code=404, detail="Invalid referral code")

    return {
        "id": admin.id,
        "name": admin.name,
        "referral_code": admin.referral_code,
    }


@router.get("/link/{code}")
def referral_redirect(code: str, db: Session = Depends(get_db)):
    admin = db.query(User).filter(
        User.referral_code == code,
        User.role == UserRole.admin,
    ).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Invalid referral link")

    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return RedirectResponse(url=f"{FRONTEND_URL}/register?ref={code}")
