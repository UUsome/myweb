from __future__ import annotations

from typing import Protocol

from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.core.base_model import CoreModel


class Like(CoreModel):
    """Polymorphic like model. Can like posts, replies, etc."""

    __tablename__ = "interaction_likes"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "target_type", "target_id",
            name="uq_user_target_like",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    target_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    target_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )

    # Relationship
    user: Mapped["User"] = relationship("User", lazy="selectin")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return (
            f"<Like(id={self.id}, user_id={self.user_id}, "
            f"target={self.target_type}:{self.target_id})>"
        )


class Comment(CoreModel):
    """Polymorphic comment model with hierarchical support (max 3 levels)."""

    __tablename__ = "interaction_comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    target_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True
    )
    target_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("interaction_comments.id"), nullable=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    depth: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", lazy="selectin")  # type: ignore[name-defined]
    children: Mapped[list[Comment]] = relationship(
        "Comment",
        backref="parent",
        remote_side="Comment.id",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<Comment(id={self.id}, user_id={self.user_id}, "
            f"target={self.target_type}:{self.target_id}, depth={self.depth})>"
        )


class TargetValidator(Protocol):
    """Protocol for validating that a target (target_type, target_id) exists.
    
    Each app (e.g., forum) implements this to validate its own models.
    """

    async def __call__(self, target_type: str, target_id: int) -> bool: ...
