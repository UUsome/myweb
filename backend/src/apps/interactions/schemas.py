from __future__ import annotations

from pydantic import Field

from src.apps.core.base_schema import CoreSchema, TimestampSchema


# ── Like ──


class LikeStatusResponse(CoreSchema):
    is_liked: bool = False
    like_count: int = 0


class LikeCountResponse(CoreSchema):
    target_type: str
    target_id: int
    like_count: int = 0


# ── Comment ──


class CommentCreate(CoreSchema):
    content: str = Field(..., min_length=1, max_length=5000)
    parent_id: int | None = Field(
        None, description="父评论 ID，用于回复评论"
    )


class CommentResponse(TimestampSchema):
    id: int
    user_id: int
    target_type: str
    target_id: int
    parent_id: int | None = None
    content: str
    depth: int = 0
    username: str = ""
    nickname: str | None = None
    avatar_url: str | None = None
    children: list[CommentResponse] = []
