import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserRole
from app.schemas import AdminLoginRequest, TokenResponse, AdminInfo, FriendListResponse, FriendResponse
from app.utils import create_access_token, verify_access_token, verify_password

security = HTTPBearer()

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=TokenResponse)
def admin_login(body: AdminLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.username == body.username,
        User.role == UserRole.admin
    ).first()

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return create_access_token(user.id)


@router.get("/me", response_model=AdminInfo)
def admin_me(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user_id = verify_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    BASE = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "referral_code": user.referral_code,
        "referral_count": db.query(User).filter(User.referred_by_id == user.id).count(),
        "referral_link": f"{BASE}/register?ref={user.referral_code}",
    }


@router.get("/{admin_id}/friends", response_model=FriendListResponse)
def admin_friends(
    admin_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials
    caller_id = verify_access_token(token)
    caller = db.query(User).filter(User.id == caller_id).first()
    if not caller or caller.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admins only")

    admin = db.query(User).filter(User.id == admin_id, User.role == UserRole.admin).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    friends = db.query(User).filter(User.referred_by_id == admin_id).all()

    return {
        "admin_id": admin.id,
        "admin_name": admin.name,
        "total": len(friends),
        "friends": friends,
    }
