from __future__ import annotations

from enum import Enum as PyEnum

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.apps.core.base_model import CoreModel


class UserRole(str, PyEnum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    MEMBER = "member"


class UserStatus(str, PyEnum):
    ACTIVE = "active"
    FROZEN = "frozen"


class User(CoreModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        String(20), default=UserRole.MEMBER, nullable=False
    )
    status: Mapped[UserStatus] = mapped_column(
        String(20), default=UserStatus.ACTIVE, nullable=False, index=True
    )
    phone: Mapped[str | None] = mapped_column(
        String(20), nullable=True, index=True
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    @property
    def is_frozen(self) -> bool:
        return self.status == UserStatus.FROZEN

    @property
    def is_active_user(self) -> bool:
        return self.status == UserStatus.ACTIVE and self.deleted_at is None
