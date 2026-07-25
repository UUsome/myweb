from __future__ import annotations

from enum import Enum as PyEnum

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.core.base_model import CoreModel


class PostStatus(str, PyEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    PINNED = "pinned"
    ESSENCE = "essence"


class Category(CoreModel):
    __tablename__ = "forum_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("forum_categories.id"), nullable=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    children: Mapped[list[Category]] = relationship(
        "Category",
        backref="parent",
        remote_side="Category.id",
        lazy="selectin",
    )
    posts: Mapped[list["Post"]] = relationship(
        "Post", back_populates="category", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name={self.name}, slug={self.slug})>"


class Post(CoreModel):
    __tablename__ = "forum_posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("forum_categories.id"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    status: Mapped[PostStatus] = mapped_column(
        String(20), default=PostStatus.PUBLISHED, nullable=False, index=True
    )
    like_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    attachments: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    category: Mapped[Category] = relationship("Category", back_populates="posts")
    user: Mapped["User"] = relationship("User", lazy="selectin")  # type: ignore[name-defined]
    replies: Mapped[list["Reply"]] = relationship(
        "Reply", back_populates="post", lazy="selectin",
        order_by="Reply.created_at.asc()",
    )

    def __repr__(self) -> str:
        return f"<Post(id={self.id}, title={self.title}, status={self.status})>"


class Reply(CoreModel):
    __tablename__ = "forum_replies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("forum_posts.id"), nullable=False, index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comment_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    post: Mapped[Post] = relationship("Post", back_populates="replies")
    user: Mapped["User"] = relationship("User", lazy="selectin")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Reply(id={self.id}, post_id={self.post_id})>"
