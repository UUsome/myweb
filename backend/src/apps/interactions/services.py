from __future__ import annotations

from typing import Protocol

from sqlalchemy import func as sa_func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.interactions.models import Comment, Like
from src.apps.interactions.schemas import CommentResponse, LikeStatusResponse
from src.core.logger import get_logger

logger = get_logger(__name__)


# ── Like Services ──


async def toggle_like(
    db: AsyncSession,
    user_id: int,
    target_type: str,
    target_id: int,
) -> tuple[bool, int]:
    """Toggle like status. Returns (is_liked_now, like_count)."""
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.target_type == target_type,
        Like.target_id == target_id,
        Like.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        # Unlike: soft delete
        from src.apps.core.base_repository import BaseRepository

        class LikeRepo(BaseRepository):
            model = Like

        await LikeRepo.soft_delete(db, existing.id)
        is_liked = False
    else:
        # Like
        like = Like(user_id=user_id, target_type=target_type, target_id=target_id)
        db.add(like)
        await db.flush()
        is_liked = True

    # Get current count
    count_stmt = select(sa_func.count()).select_from(Like).where(
        Like.target_type == target_type,
        Like.target_id == target_id,
        Like.deleted_at.is_(None),
    )
    count_result = await db.execute(count_stmt)
    like_count = count_result.scalar_one()

    # Async update the target's like_count
    await _update_target_like_count(db, target_type, target_id, like_count)

    return is_liked, like_count


async def get_like_status(
    db: AsyncSession,
    user_id: int,
    target_type: str,
    target_id: int,
) -> LikeStatusResponse:
    """Get like status for a user on a target."""
    stmt = select(Like).where(
        Like.user_id == user_id,
        Like.target_type == target_type,
        Like.target_id == target_id,
        Like.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    is_liked = result.scalar_one_or_none() is not None

    count_stmt = select(sa_func.count()).select_from(Like).where(
        Like.target_type == target_type,
        Like.target_id == target_id,
        Like.deleted_at.is_(None),
    )
    count_result = await db.execute(count_stmt)
    like_count = count_result.scalar_one()

    return LikeStatusResponse(is_liked=is_liked, like_count=like_count)


async def get_like_count(
    db: AsyncSession,
    target_type: str,
    target_id: int,
) -> int:
    """Get like count for a target."""
    stmt = select(sa_func.count()).select_from(Like).where(
        Like.target_type == target_type,
        Like.target_id == target_id,
        Like.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def _update_target_like_count(
    db: AsyncSession,
    target_type: str,
    target_id: int,
    like_count: int,
) -> None:
    """Update like_count on the target model (post or reply)."""
    if target_type == "post":
        from src.apps.forum.models import Post

        stmt = select(Post).where(Post.id == target_id)
        result = await db.execute(stmt)
        post = result.scalar_one_or_none()
        if post:
            post.like_count = like_count
    elif target_type == "reply":
        from src.apps.forum.models import Reply

        stmt = select(Reply).where(Reply.id == target_id)
        result = await db.execute(stmt)
        reply = result.scalar_one_or_none()
        if reply:
            reply.like_count = like_count


# ── Comment Services ──

MAX_COMMENT_DEPTH = 3


async def create_comment(
    db: AsyncSession,
    user_id: int,
    target_type: str,
    target_id: int,
    content: str,
    parent_id: int | None = None,
) -> Comment:
    """Create a comment. Validates depth constraint."""
    depth = 0
    if parent_id:
        stmt = select(Comment).where(
            Comment.id == parent_id,
            Comment.deleted_at.is_(None),
        )
        result = await db.execute(stmt)
        parent = result.scalar_one_or_none()
        if parent is None:
            raise ValueError("父评论不存在")
        depth = parent.depth + 1
        if depth >= MAX_COMMENT_DEPTH:
            raise ValueError(f"评论深度不能超过 {MAX_COMMENT_DEPTH} ")

    comment = Comment(
        user_id=user_id,
        target_type=target_type,
        target_id=target_id,
        parent_id=parent_id,
        content=content,
        depth=depth,
    )
    db.add(comment)
    await db.flush()
    await db.refresh(comment)

    # Update comment count on target
    await _update_target_comment_count(db, target_type, target_id)

    return comment


async def get_comments(
    db: AsyncSession,
    target_type: str,
    target_id: int,
) -> list[CommentResponse]:
    """Get all comments for a target, structured as a tree."""
    stmt = (
        select(Comment)
        .options(joinedload(Comment.user), joinedload(Comment.children))
        .where(
            Comment.target_type == target_type,
            Comment.target_id == target_id,
            Comment.deleted_at.is_(None),
            Comment.parent_id.is_(None),  # Top-level only
        )
        .order_by(Comment.created_at.asc())
    )
    result = await db.execute(stmt)
    comments = result.scalars().unique().all()

    return [_build_comment_tree(c) for c in comments]


def _build_comment_tree(comment: Comment) -> CommentResponse:
    """Recursively build comment tree."""
    children = []
    if comment.children:
        for child in sorted(
            comment.children,
            key=lambda c: c.created_at or "",
        ):
            if child.deleted_at is None:
                children.append(_build_comment_tree(child))

    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        target_type=comment.target_type,
        target_id=comment.target_id,
        parent_id=comment.parent_id,
        content=comment.content,
        depth=comment.depth,
        created_at=comment.created_at,
        updated_at=comment.updated_at,
        username=comment.user.username if comment.user else "",
        nickname=comment.user.nickname if comment.user else None,
        avatar_url=comment.user.avatar_url if comment.user else None,
        children=children,
    )


async def delete_comment(
    db: AsyncSession, comment_id: int, user_id: int, is_admin: bool = False
) -> bool:
    """Delete a comment (soft delete). Only author or admin can delete."""
    stmt = select(Comment).where(
        Comment.id == comment_id,
        Comment.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    comment = result.scalar_one_or_none()
    if comment is None:
        return False

    if comment.user_id != user_id and not is_admin:
        return False
    from src.apps.core.base_repository import BaseRepository

    class CommentRepo(BaseRepository):
        model = Comment

    deleted = await CommentRepo.soft_delete(db, comment_id)
    if deleted:
        await _update_target_comment_count(
            db, comment.target_type, comment.target_id
        )
    return deleted is not None


async def _update_target_comment_count(
    db: AsyncSession,
    target_type: str,
    target_id: int,
) -> None:
    """Update comment_count on the target model."""
    if target_type == "post":
        from src.apps.forum.models import Post

        count_stmt = select(sa_func.count()).select_from(Comment).where(
            Comment.target_type == target_type,
            Comment.target_id == target_id,
            Comment.deleted_at.is_(None),
        )
        count_result = await db.execute(count_stmt)
        count = count_result.scalar_one()

        stmt = select(Post).where(Post.id == target_id)
        result = await db.execute(stmt)
        post = result.scalar_one_or_none()
        if post:
            post.comment_count = count
