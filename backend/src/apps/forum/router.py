from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.core.pagination import CursorPage, paginate_cursor
from src.apps.core.response import APIResponse, success
from src.apps.forum import services as forum_services
from src.apps.forum.dependencies import validate_forum_target
from src.apps.forum.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    PostCreate,
    PostDetailResponse,
    PostListResponse,
    PostUpdate,
    ReplyCreate,
    ReplyResponse,
)
from src.apps.users.dependencies import get_current_admin_user, get_current_user
from src.apps.users.models import User, UserRole
from src.core.database import get_db
from src.core.logger import get_logger

from .exceptions import Forbidden, NotFound

logger = get_logger(__name__)

router = APIRouter(tags=["Forum"])


# ── Categories ──


@router.get(
    "/categories",
    summary="获取板块",
    description="获取所有板块的树形结构（带缓存，TTL 5分钟",
)
async def get_categories(
    db: AsyncSession = Depends(get_db),
) -> APIResponse[list[CategoryResponse]]:
    tree = await forum_services.get_category_tree(db)
    return success(data=tree)


@router.post(
    "/categories",
    summary="创建板块",
    description="创建新板块（管理员）",
)
async def create_category(
    req: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[CategoryResponse]:
    category = await forum_services.create_category(db, req.model_dump())
    return success(
        data=CategoryResponse.model_validate(category),
        message="板块创建成功",
    )


@router.put(
    "/categories/{category_id}",
    summary="更新板块",
    description="更新板块信息（管理员",
)
async def update_category(
    category_id: int,
    req: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[CategoryResponse]:
    category = await forum_services.update_category(
        db, category_id, req.model_dump(exclude_unset=True)
    )
    if category is None:
        raise NotFound(message="板块不存")
    return success(
        data=CategoryResponse.model_validate(category),
        message="板块更新成功",
    )


@router.delete(
    "/categories/{category_id}",
    summary="删除板块",
    description="删除板块（管理员，软删除",
)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[None]:
    deleted = await forum_services.delete_category(db, category_id)
    if not deleted:
        raise NotFound(message="板块不存")
    return success(message="板块删除成功")


# ── Posts ──


@router.get(
    "/posts",
    summary="帖子列表",
    description="帖子列表，支持按板块/状态筛选和游标分页",
)
async def list_posts(
    category_id: int | None = None,
    status: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[CursorPage[PostListResponse]]:
    items, next_cursor, has_next = await forum_services.list_posts(
        db, category_id, status, cursor, limit
    )
    return success(
        data=CursorPage(list=items, cursor=next_cursor, has_next=has_next)
    )


@router.get(
    "/posts/{post_id}",
    summary="帖子详情",
    description="获取帖子详细内容",
)
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[PostDetailResponse]:
    post = await forum_services.get_post_detail(db, post_id)
    if post is None:
        raise NotFound(message="帖子不存")
    return success(data=post)


@router.post(
    "/posts",
    summary="发布帖子",
    description="发布新帖子（需登录",
)
async def create_post(
    req: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[PostDetailResponse]:
    post = await forum_services.create_post(db, current_user.id, req)
    detail = await forum_services.get_post_detail(db, post.id)
    return success(data=detail, message="帖子发布成功")


@router.put(
    "/posts/{post_id}",
    summary="编辑帖子",
    description="编辑帖子内容（作管理员）",
)
async def update_post(
    post_id: int,
    req: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[PostDetailResponse]:
    post = await forum_services.get_post_detail(db, post_id)
    if post is None:
        raise NotFound(message="帖子不存")

    if post.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise Forbidden(message="无权编辑此帖")

    updated = await forum_services.update_post(
        db, post_id, req.model_dump(exclude_unset=True)
    )
    if updated is None:
        raise NotFound(message="帖子不存")
    detail = await forum_services.get_post_detail(db, post_id)
    return success(data=detail, message="帖子更新成功")


@router.delete(
    "/posts/{post_id}",
    summary="删除帖子",
    description="删除帖子（管理员，软删除）",
)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[None]:
    from src.apps.core.base_repository import BaseRepository
    from src.apps.forum.models import Post as PostModel

    post = await forum_services.get_post_detail(db, post_id)
    if post is None:
        raise NotFound(message="帖子不存")

    if post.user_id != current_user.id and current_user.role != UserRole.ADMIN:
        raise Forbidden(message="无权删除此帖")

    class PostRepo(BaseRepository):
        model = PostModel

    result = await PostRepo.soft_delete(db, post_id)
    if result is None:
        raise NotFound(message="帖子不存")
    return success(message="帖子删除成功")


# ── Replies ──


@router.get(
    "/posts/{post_id}/replies",
    summary="帖子回复列表",
    description="获取帖子的回复列表（游标分页",
)
async def list_replies(
    post_id: int,
    cursor: str | None = None,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[CursorPage[ReplyResponse]]:
    items, next_cursor, has_next = await forum_services.list_replies(
        db, post_id, cursor, limit
    )
    return success(
        data=CursorPage(list=items, cursor=next_cursor, has_next=has_next)
    )


@router.post(
    "/posts/{post_id}/replies",
    summary="发表回复",
    description="对帖子发表回复（需登录",
)
async def create_reply(
    post_id: int,
    req: ReplyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[ReplyResponse]:
    reply = await forum_services.create_reply(db, post_id, current_user.id, req.content)
    return success(
        data=ReplyResponse(
            id=reply.id,
            post_id=reply.post_id,
            user_id=reply.user_id,
            content=reply.content,
            like_count=reply.like_count,
            comment_count=reply.comment_count,
            created_at=reply.created_at,
            updated_at=reply.updated_at,
            username=current_user.username,
            nickname=current_user.nickname,
        ),
        message="回复发表成功",
    )
