from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.site import AdminSite, ModelAdmin
from src.apps.interactions.models import Comment, Like
from src.core.database import async_session_factory
from src.core.logger import get_logger

logger = get_logger(__name__)


def register_admin(site: AdminSite) -> None:
    @site.register(Like)
    class LikeAdmin(ModelAdmin):
        list_display = [
            "id", "user_id", "target_type", "target_id", "created_at"
        ]
        list_filter = {"target_type": ["post", "reply"]}
        list_per_page = 20

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Like)
                .where(Like.deleted_at.is_(None))
                .order_by(Like.id.desc())
            )
            result = await db.execute(stmt)
            likes = result.scalars().all()
            return [
                {
                    "id": l.id,
                    "user_id": l.user_id,
                    "target_type": l.target_type,
                    "target_id": l.target_id,
                    "created_at": l.created_at.isoformat() if l.created_at else None,
                    "updated_at": l.updated_at.isoformat() if l.updated_at else None,
                }
                for l in likes
            ]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            raise NotImplementedError("Cannot create likes via admin")


        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class LikeRepo(BaseRepository):
                model = Like

            async with async_session_factory() as db:
                try:
                    result = await LikeRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise


    @site.register(Comment)
    class CommentAdmin(ModelAdmin):
        list_display = [
            "id", "user_id", "target_type", "target_id",
            "depth", "created_at"
        ]
        list_filter = {"target_type": ["post", "reply"]}
        search_fields = ["content"]
        list_per_page = 20

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Comment)
                .where(Comment.deleted_at.is_(None))
                .order_by(Comment.id.desc())
            )
            result = await db.execute(stmt)
            comments = result.scalars().all()
            return [
                {
                    "id": c.id,
                    "user_id": c.user_id,
                    "target_type": c.target_type,
                    "target_id": c.target_id,
                    "content": c.content[:100],
                    "depth": c.depth,
                    "parent_id": c.parent_id,
                    "created_at": c.created_at.isoformat() if c.created_at else None,
                    "updated_at": c.updated_at.isoformat() if c.updated_at else None,
                }
                for c in comments
            ]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            raise NotImplementedError("Cannot create likes via admin")


        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class CommentRepo(BaseRepository):
                model = Comment

            async with async_session_factory() as db:
                try:
                    result = await CommentRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise
