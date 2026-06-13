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
