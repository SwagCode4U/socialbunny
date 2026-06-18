

Zeel: 
Schemas
   class AdminInfo(BaseModel):
    id: int
    username: str
    name: str
    email: Optional[str] = None
    role: str
    referral_code: str
    referral_count: int
    referral_link : str 





# ------------- referral ----------------------------
class ReferralLookupResponse(BaseModel):
    id: int
    name: str
    referral_code: str

class FriendResponse(BaseModel):
    id : int 
    name : str 
    email : str = None
    created_at: datetime
    class Config:
        from_attributes = True

    
class FriendListResponse(BaseModel):
    admin_id: int 
    admin_name: str 
    total: int 
    friends: list[FriendResponse]




# auth_routes
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db 
from app.models import User, UserRole
from app.schemas import AdminLoginRequest, TokenResponse, AdminInfo , ReferralLookupResponse , FriendResponse , FriendListResponse
from app.utils import create_access_token, verify_access_token, verify_password

router = APIRouter(prefix="/api/admin", tags=["admin"])
BASE_URL="http://127.0.0.1:8000"

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
def admin_me(token: str, db: Session = Depends(get_db)):
    user_id = verify_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user or user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admins only")
    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "referral_code": user.referral_code,
        "referral_count": db.query(User).filter(User.referred_by_id == user.id).count(),
        "referral_link":f"{BASE_URL}/api/admin/register/{user.referral_code}"
    }


@router.get("/register/{referral_code}",response_model= ReferralLookupResponse)
def get_referral_user(referral_code:str , db : Session = Depends(get_db)):
    user =  db.query(User).filter(User.referral_code == referral_code).first()
    if not user:
        raise HTTPException (
            status_code= 404,
            detail="Invalid referral code"
        )
    return user

@router.get("/referrals",response_model=list[FriendResponse])
def get_my_referrals(token:str,db:Session = Depends(get_db)):
    user_id = verify_access_token(token)

    user = db.query(User).filter(User.id == user_id).first()

    if not user or user.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Admins only!"

        )

    referrals = db.query(User).filter(User.referred_by_id == user.id).all()

    return referrals




@router.get("/friends",response_model=FriendListResponse)
def admin_friends(token:str, db:Session = Depends (get_db)):
    user_id = verify_access_token(token)
    admin = db.query(User).filter(User.id == user_id).first()


    if not admin or admin.role != UserRole.admin:
        raise HTTPException(
            status_code=403,
            detail="Admins only!"

        )

    friends = db.query(User).filter(User.referred_by_id == user_id).all()

    return {
        "admin_id": admin.id,
        "admin_name": admin.name,
        "total": len(friends),
        "friends":friends
    }


# Referal
