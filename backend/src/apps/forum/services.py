from __future__ import annotations

import time
from typing import Any

from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.forum.models import Category, Post, PostStatus, Reply
from src.apps.forum.schemas import (
    CategoryResponse,
    PostCreate,
    PostDetailResponse,
    PostListResponse,
    ReplyResponse,
)
from src.core.config import settings
from src.core.logger import get_logger

logger = get_logger(__name__)

# ── Category Cache ──

_category_cache: dict[str, Any] = {"data": None, "expires_at": 0}


def _get_cached_categories() -> list[CategoryResponse] | None:
    if _category_cache["data"] and time.time() < _category_cache["expires_at"]:
        return _category_cache["data"]
    return None


def _set_cached_categories(categories: list[CategoryResponse]) -> None:
    _category_cache["data"] = categories
    _category_cache["expires_at"] = time.time() + settings.CATEGORY_CACHE_TTL


def invalidate_category_cache() -> None:
    _category_cache["data"] = None
    _category_cache["expires_at"] = 0


def _build_category_tree(
    categories: list[Category], parent_id: int | None = None
) -> list[CategoryResponse]:
    tree: list[CategoryResponse] = []
    for cat in categories:
        if cat.parent_id == parent_id:
            children = _build_category_tree(categories, cat.id)
            tree.append(
                CategoryResponse(
                    id=cat.id,
                    name=cat.name,
                    slug=cat.slug,
                    parent_id=cat.parent_id,
                    description=cat.description,
                    sort_order=cat.sort_order,
                    created_at=cat.created_at,
                    updated_at=cat.updated_at,
                    children=children,
                )
            )
    tree.sort(key=lambda c: c.sort_order)
    return tree


# ── Category Services ──


async def get_category_tree(db: AsyncSession) -> list[CategoryResponse]:
    cached = _get_cached_categories()
    if cached is not None:
        return cached

    stmt = (
        select(Category)
        .where(Category.deleted_at.is_(None))
        .order_by(Category.sort_order)
    )
    result = await db.execute(stmt)
    categories = list(result.scalars().all())

    tree = _build_category_tree(categories)
    _set_cached_categories(tree)
    return tree


async def create_category(db: AsyncSession, data: dict[str, Any]) -> Category:
    category = Category(**data)
    db.add(category)
    await db.flush()
    await db.refresh(category)
    invalidate_category_cache()
    return category


async def update_category(
    db: AsyncSession, category_id: int, data: dict[str, Any]
) -> Category | None:
    stmt = select(Category).where(
        Category.id == category_id,
        Category.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    category = result.scalar_one_or_none()
    if category is None:
        return None
    for field, value in data.items():
        setattr(category, field, value)
    await db.flush()
    await db.refresh(category)
    invalidate_category_cache()
    return category


async def delete_category(db: AsyncSession, category_id: int) -> bool:
    from src.apps.core.base_repository import BaseRepository

    class CategoryRepo(BaseRepository):
        model = Category

    result = await CategoryRepo.soft_delete(db, category_id)
    invalidate_category_cache()
    return result is not None


# ── Post Services ──


async def list_posts(
    db: AsyncSession,
    category_id: int | None = None,
    status: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[PostListResponse], str | None, bool]:
    stmt = (
        select(Post)
        .options(joinedload(Post.category), joinedload(Post.user))
        .where(Post.deleted_at.is_(None))
    )

    if category_id:
        stmt = stmt.where(Post.category_id == category_id)
    if status:
        stmt = stmt.where(Post.status == status)
    else:
        stmt = stmt.where(Post.status.in_([PostStatus.PUBLISHED, PostStatus.PINNED, PostStatus.ESSENCE]))

    if cursor:
        stmt = stmt.where(Post.id < int(cursor))

    stmt = stmt.order_by(Post.id.desc()).limit(limit + 1)

    result = await db.execute(stmt)
    posts = list(result.scalars().unique().all())

    has_next = len(posts) > limit
    if has_next:
        posts = posts[:limit]

    next_cursor: str | None = None
    if posts and has_next:
        next_cursor = str(posts[-1].id)

    items = [
        PostListResponse(
            id=p.id,
            title=p.title,
            category_id=p.category_id,
            user_id=p.user_id,
            status=p.status,
            like_count=p.like_count,
            comment_count=p.comment_count,
            created_at=p.created_at,
            updated_at=p.updated_at,
            username=p.user.username if p.user else "",
            nickname=p.user.nickname if p.user else None,
            category_name=p.category.name if p.category else "",
        )
        for p in posts
    ]

    return items, next_cursor, has_next


async def get_post_detail(
    db: AsyncSession, post_id: int
) -> PostDetailResponse | None:
    stmt = (
        select(Post)
        .options(joinedload(Post.category), joinedload(Post.user))
        .where(Post.id == post_id, Post.deleted_at.is_(None))
    )
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post is None:
        return None

    return PostDetailResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        category_id=post.category_id,
        user_id=post.user_id,
        status=post.status,
        like_count=post.like_count,
        comment_count=post.comment_count,
        attachments=post.attachments,
        created_at=post.created_at,
        updated_at=post.updated_at,
        username=post.user.username if post.user else "",
        nickname=post.user.nickname if post.user else None,
        category_name=post.category.name if post.category else "",
    )


async def create_post(db: AsyncSession, user_id: int, data: PostCreate) -> Post:
    post = Post(
        title=data.title,
        content=data.content,
        category_id=data.category_id,
        user_id=user_id,
        status=data.status,
        attachments=data.attachments,
    )
    db.add(post)
    await db.flush()
    await db.refresh(post)
    return post


async def update_post(
    db: AsyncSession, post_id: int, data: dict[str, Any]
) -> Post | None:
    stmt = select(Post).where(
        Post.id == post_id,
        Post.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post is None:
        return None
    for field, value in data.items():
        setattr(post, field, value)
    await db.flush()
    await db.refresh(post)
    return post


# ── Reply Services ──


async def list_replies(
    db: AsyncSession, post_id: int, cursor: str | None = None, limit: int = 20
) -> tuple[list[ReplyResponse], str | None, bool]:
    stmt = (
        select(Reply)
        .options(joinedload(Reply.user))
        .where(Reply.post_id == post_id, Reply.deleted_at.is_(None))
    )
    if cursor:
        stmt = stmt.where(Reply.id > int(cursor))

    stmt = stmt.order_by(Reply.id.asc()).limit(limit + 1)

    result = await db.execute(stmt)
    replies = list(result.scalars().unique().all())

    has_next = len(replies) > limit
    if has_next:
        replies = replies[:limit]

    next_cursor: str | None = None
    if replies and has_next:
        next_cursor = str(replies[-1].id)

    items = [
        ReplyResponse(
            id=r.id,
            post_id=r.post_id,
            user_id=r.user_id,
            content=r.content,
            like_count=r.like_count,
            comment_count=r.comment_count,
            created_at=r.created_at,
            updated_at=r.updated_at,
            username=r.user.username if r.user else "",
            nickname=r.user.nickname if r.user else None,
        )
        for r in replies
    ]

    return items, next_cursor, has_next


async def create_reply(
    db: AsyncSession, post_id: int, user_id: int, content: str
) -> Reply:
    reply = Reply(post_id=post_id, user_id=user_id, content=content)
    db.add(reply)
    await db.flush()
    await db.refresh(reply)

    # Update post comment count
    stmt = select(Post).where(Post.id == post_id)
    result = await db.execute(stmt)
    post = result.scalar_one_or_none()
    if post:
        post.comment_count = (
            await db.execute(
                select(sa_func.count()).select_from(Reply).where(
                    Reply.post_id == post_id,
                    Reply.deleted_at.is_(None),
                )
            )
        ).scalar_one()

    return reply
