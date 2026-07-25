from __future__ import annotations

from typing import Any

from pydantic import Field

from src.apps.core.base_schema import CoreSchema, TimestampSchema

from .models import UserRole, UserStatus


class LoginRequest(CoreSchema):
    username: str = Field(..., min_length=1, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=128, description="密码")


class TokenResponse(CoreSchema):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(CoreSchema):
    refresh_token: str


class UserBase(CoreSchema):
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., max_length=255)
    nickname: str | None = Field(None, max_length=100)
    avatar_url: str | None = Field(None, max_length=500)
    role: UserRole = UserRole.MEMBER
    status: UserStatus = UserStatus.ACTIVE
    phone: str | None = Field(None, max_length=20)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserUpdate(CoreSchema):
    nickname: str | None = Field(None, max_length=100)
    avatar_url: str | None = Field(None, max_length=500)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=20)


class UserUpdateAdmin(CoreSchema):
    """Admin-only user update schema."""
    nickname: str | None = None
    avatar_url: str | None = None
    email: str | None = None
    role: UserRole | None = None
    status: UserStatus | None = None
    password: str | None = Field(None, min_length=6, max_length=128)


class UserResponse(TimestampSchema):
    id: int
    username: str
    email: str
    nickname: str | None = None
    avatar_url: str | None = None
    role: UserRole
    status: UserStatus
    phone: str | None = None


class UserPublicResponse(CoreSchema):
    """Public user info visible to anyone."""
    id: int
    username: str
    nickname: str | None = None
    avatar_url: str | None = None
    role: UserRole
