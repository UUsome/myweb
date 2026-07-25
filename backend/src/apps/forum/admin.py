from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.site import AdminSite, ModelAdmin
from src.apps.forum.models import Category, Post, Reply
from src.apps.forum.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
    PostDetailResponse,
    PostUpdate,
)
from src.apps.forum.services import (
    create_category,
    get_post_detail,
    update_category,
    update_post,
)
from src.core.database import async_session_factory
from src.core.logger import get_logger

logger = get_logger(__name__)


def register_admin(site: AdminSite) -> None:
    @site.register(Category)
    class CategoryAdmin(ModelAdmin):
        list_display = ["id", "name", "slug", "parent_id", "sort_order", "created_at"]
        search_fields = ["name", "slug"]
        list_per_page = 50

        model_schema_create = CategoryCreate
        model_schema_update = CategoryUpdate
        model_schema_response = CategoryResponse

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Category)
                .where(Category.deleted_at.is_(None))
                .order_by(Category.sort_order)
            )
            result = await db.execute(stmt)
            cats = result.scalars().all()
            return [CategoryResponse.model_validate(c).model_dump() for c in cats]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    cat = await create_category(db, data)
                    await db.commit()
                    return CategoryResponse.model_validate(cat).model_dump()
                except Exception:
                    await db.rollback()
                    raise



        async def update_object(
            self, id: int, data: dict[str, Any]
        ) -> dict[str, Any] | None:
            async with async_session_factory() as db:
                try:
                    cat = await update_category(db, id, data)
                    if cat is None:
                        return None
                    await db.commit()
                    return CategoryResponse.model_validate(cat).model_dump()
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class CatRepo(BaseRepository):
                model = Category

            async with async_session_factory() as db:
                try:
                    result = await CatRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

    @site.register(Post)
    class PostAdmin(ModelAdmin):
        list_display = [
            "id", "title", "category_id", "user_id", "status",
            "like_count", "comment_count", "created_at",
        ]
        list_filter = {"status": ["draft", "published", "pinned", "essence"]}
        search_fields = ["title"]
        list_per_page = 20

        model_schema_update = PostUpdate
        model_schema_response = PostDetailResponse

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Post)
                .where(Post.deleted_at.is_(None))
                .order_by(Post.id.desc())
            )
            result = await db.execute(stmt)
            posts = result.scalars().all()
            items = []
            for p in posts:
                detail = await get_post_detail(db, p.id)
                if detail:
                    items.append(detail.model_dump())
            return items

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    from src.apps.forum.services import create_post
                    post = await create_post(db, data)
                    await db.commit()
                    detail = await get_post_detail(db, post.id)
                    return detail.model_dump() if detail else {}
                except Exception:
                    await db.rollback()
                    raise

        async def update_object(
            self, id: int, data: dict[str, Any]
        ) -> dict[str, Any] | None:
            async with async_session_factory() as db:
                try:
                    post = await update_post(db, id, data)
                    if post is None:
                        return None
                    await db.commit()
                    detail = await get_post_detail(db, id)
                    return detail.model_dump() if detail else None
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class PostRepo(BaseRepository):
                model = Post

            async with async_session_factory() as db:
                try:
                    result = await PostRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

    @site.register(Reply)
    class ReplyAdmin(ModelAdmin):
        list_display = ["id", "post_id", "user_id", "created_at"]
        search_fields = ["content"]
        list_per_page = 20

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Reply)
                .where(Reply.deleted_at.is_(None))
                .order_by(Reply.id.desc())
            )
            result = await db.execute(stmt)
            replies = result.scalars().all()
            return [
                {
                    "id": r.id,
                    "post_id": r.post_id,
                    "user_id": r.user_id,
                    "content": r.content[:100],
                    "like_count": r.like_count,
                    "comment_count": r.comment_count,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "updated_at": r.updated_at.isoformat() if r.updated_at else None,
                }
                for r in replies
            ]

        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class ReplyRepo(BaseRepository):
                model = Reply

            async with async_session_factory() as db:
                try:
                    result = await ReplyRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

