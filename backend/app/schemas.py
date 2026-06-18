from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ── Project (existing) ───────────────────────────────────────

class ProjectBase(BaseModel):
    name: str
    description: str
    backend_framework: str
    frontend_framework: str

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Super Admin Login ────────────────────────────────────────

class AdminLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class AdminInfo(BaseModel):
    id: int
    username: str
    name: str
    email: Optional[str] = None
    role: str
    referral_code: str
    referral_count: int
    referral_link: str


# ── Google OAuth ─────────────────────────────────────────────

class GoogleAuthRequest(BaseModel):
    id_token: str

class ReferralLookupResponse(BaseModel):
    id: int
    name: str
    referral_code: str


# ── Onboarding Wizard ────────────────────────────────────────

class WizardUpdate(BaseModel):
    name: str
    phone: str
    interest: str
    referred_by_id: Optional[int] = None


# ── User Response ────────────────────────────────────────────

class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    name: str
    picture: Optional[str] = None
    role: str
    phone: Optional[str] = None
    interest: Optional[str] = None
    referred_by_id: Optional[int] = None
    is_onboarded: bool

    class Config:
        from_attributes = True


# ── Students Corner ──────────────────────────────────────────

class TopicCreate(BaseModel):
    title: str
    content: str
    author: str

class TopicPreview(BaseModel):
    id: int
    title: str
    author: str
    created_at: datetime
    preview: str

class TopicDetail(BaseModel):
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TopicListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    topics: list[TopicPreview]


# ── News Feeder ──────────────────────────────────────────────

class NewsItem(BaseModel):
    title: str
    link: str
    summary: str
    published: Optional[str] = None
    published_parsed: Optional[str] = None

class NewsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[NewsItem]


# ── Google Auth Response (includes JWT) ─────────────────────

class GoogleAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# ── Admin's Friends List ─────────────────────────────────────

class FriendResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class FriendListResponse(BaseModel):
    admin_id: int
    admin_name: str
    total: int
    friends: list[FriendResponse]
