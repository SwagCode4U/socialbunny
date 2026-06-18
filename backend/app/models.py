from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from app.database import Base
import enum


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    backend_framework = Column(String(50))
    frontend_framework = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class UserRole(str, enum.Enum):
    student = "student"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, index=True, nullable=True)
    google_sub = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(100), index=True)
    picture = Column(String(500))
    password_hash = Column(String(255), nullable=True)
    role = Column(SAEnum(UserRole), default=UserRole.student)
    phone = Column(String(20), nullable=True)
    interest = Column(String(50), nullable=True)
    referral_code = Column(String(20), unique=True, index=True, nullable=True)
    referred_by_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    referred_by = relationship(
        "User",
        remote_side="User.id",
        backref=backref("referrals", lazy="dynamic"),
    )

    @property
    def is_onboarded(self) -> bool:
        return bool(self.phone and self.interest)


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True)
    content = Column(Text)
    author = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

