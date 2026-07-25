from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from src.apps.core.base_schema import CoreSchema, TimestampSchema

from .models import PostStatus


# ── Category ──


class CategoryBase(CoreSchema):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    parent_id: int | None = None
    description: str | None = None
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CoreSchema):
    name: str | None = None
    slug: str | None = None
    parent_id: int | None = None
    description: str | None = None
    sort_order: int | None = None


class CategoryResponse(TimestampSchema):
    id: int
    name: str
    slug: str
    parent_id: int | None = None
    description: str | None = None
    sort_order: int = 0
    # children: list[CategoryResponse] = [] | None = None
    children: list["CategoryResponse"] | None = None

# ── Post ──


class PostBase(CoreSchema):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category_id: int
    attachments: dict[str, Any] | None = None


class PostCreate(PostBase):
    status: PostStatus = PostStatus.PUBLISHED


class PostUpdate(CoreSchema):
    title: str | None = Field(None, max_length=200)
    content: str | None = None
    category_id: int | None = None
    status: PostStatus | None = None
    attachments: dict[str, Any] | None = None


class PostListResponse(TimestampSchema):
    id: int
    title: str
    category_id: int
    user_id: int
    status: PostStatus
    like_count: int = 0
    comment_count: int = 0
    username: str = ""
    nickname: str | None = None
    category_name: str = ""


class PostDetailResponse(TimestampSchema):
    id: int
    title: str
    content: str
    category_id: int
    user_id: int
    status: PostStatus
    like_count: int = 0
    comment_count: int = 0
    attachments: dict[str, Any] | None = None
    username: str = ""
    nickname: str | None = None
    category_name: str = ""


# ── Reply ──


class ReplyCreate(CoreSchema):
    content: str = Field(..., min_length=1)


class ReplyResponse(TimestampSchema):
    id: int
    post_id: int
    user_id: int
    content: str
    like_count: int = 0
    comment_count: int = 0
    username: str = ""
    nickname: str | None = None
