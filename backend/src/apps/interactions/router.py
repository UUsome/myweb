from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.core.response import APIResponse, success
from src.apps.interactions import services as interaction_services
from src.apps.interactions.dependencies import verify_target_exists
from src.apps.interactions.schemas import (
    CommentCreate,
    CommentResponse,
    LikeCountResponse,
    LikeStatusResponse,
)
from src.apps.users.dependencies import get_current_user
from src.apps.users.models import User, UserRole
from src.core.database import get_db
from src.core.logger import get_logger

from .exceptions import Forbidden, NotFound

logger = get_logger(__name__)

router = APIRouter(tags=["Interactions"])


# ── Likes ──


@router.post(
    "/like/{target_type}/{target_id}",
    summary="点赞/取消点赞",
    description="切换点赞状态，已点赞则取消，未点赞则添加（需登录)",
    response_model=None,
)
async def toggle_like(
    target: tuple[str, int] = Depends(verify_target_exists),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[LikeStatusResponse]:
    target_type, target_id = target
    is_liked, like_count = await interaction_services.toggle_like(
        db, current_user.id, target_type, target_id
    )
    return success(
        data=LikeStatusResponse(is_liked=is_liked, like_count=like_count)
    )


@router.get(
    "/like/{target_type}/{target_id}/status",
    summary="获取点赞状",
    description="获取当前用户对目标的点赞状态和点赞数（需登录)",
)
async def get_like_status(
    target: tuple[str, int] = Depends(verify_target_exists),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[LikeStatusResponse]:
    target_type, target_id = target
    status = await interaction_services.get_like_status(
        db, current_user.id, target_type, target_id
    )
    return success(data=status)


@router.get(
    "/like/{target_type}/{target_id}/count",
    summary="获取点赞",
    description="公开接口，获取目标的点赞总数",
)
async def get_like_count(
    target: tuple[str, int] = Depends(verify_target_exists),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[LikeCountResponse]:
    target_type, target_id = target
    count = await interaction_services.get_like_count(db, target_type, target_id)
    return success(
        data=LikeCountResponse(
            target_type=target_type,
            target_id=target_id,
            like_count=count,
        )
    )


# ── Comments ──


@router.get(
    "/comments/{target_type}/{target_id}",
    summary="获取评论列表",
    description="公开接口，获取目标的所有评论（树形结构",
)
async def get_comments(
    target: tuple[str, int] = Depends(verify_target_exists),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[list[CommentResponse]]:
    target_type, target_id = target
    comments = await interaction_services.get_comments(db, target_type, target_id)
    return success(data=comments)


@router.post(
    "/comments/{target_type}/{target_id}",
    summary="发表评论",
    description="对目标发表评论（需登录），支持回复评论（parent_id",
)
async def create_comment(
    req: CommentCreate,
    target: tuple[str, int] = Depends(verify_target_exists),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[CommentResponse]:
    target_type, target_id = target
    try:
        comment = await interaction_services.create_comment(
            db,
            current_user.id,
            target_type,
            target_id,
            req.content,
            req.parent_id,
        )
    except ValueError as e:
        raise NotFound(message=str(e))

    # Reload with user
    from sqlalchemy.orm import joinedload
    from sqlalchemy import select

    from src.apps.interactions.models import Comment as CommentModel

    stmt = (
        select(CommentModel)
        .options(joinedload(CommentModel.user))
        .where(CommentModel.id == comment.id)
    )
    result = await db.execute(stmt)
    comment = result.scalar_one()

    return success(
        data=CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            target_type=comment.target_type,
            target_id=comment.target_id,
            parent_id=comment.parent_id,
            content=comment.content,
            depth=comment.depth,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            username=current_user.username,
            nickname=current_user.nickname,
            avatar_url=current_user.avatar_url,
        ),
        message="评论发表成功",
    )


@router.delete(
    "/comments/{comment_id}",
    summary="删除评论",
    description="删除评论（作管理员，软删除）",
)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[None]:
    is_admin = current_user.role == UserRole.ADMIN
    deleted = await interaction_services.delete_comment(
        db, comment_id, current_user.id, is_admin
    )
    if not deleted:
        raise NotFound(message="评论不存在或无权删除")
    return success(message="评论删除成功")

