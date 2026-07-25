from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.admin.site import AdminSite, ModelAdmin
from src.apps.experthub.models import Case, Expert, Platform, ServiceDefinition, TagDefinition
from src.apps.experthub.schemas import (
    CaseResponse,
    ExpertDetailResponse,
    ExpertUpdate,
    PlatformResponse,
)
from src.apps.experthub.services import (
    create_case,
    create_expert,
    create_platform,
    get_expert_detail,
    update_case,
    update_expert,
    update_platform,
    delete_platform,
    delete_case,
)
from src.core.database import async_session_factory
from src.core.logger import get_logger

logger = get_logger(__name__)


def register_admin(site: AdminSite) -> None:
    @site.register(TagDefinition)
    class TagAdmin(ModelAdmin):
        list_display = ["id", "name", "slug", "sort_order"]
        search_fields = ["name", "slug"]
        list_per_page = 50

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(TagDefinition)
                .where(TagDefinition.deleted_at.is_(None))
                .order_by(TagDefinition.sort_order)
            )
            result = await db.execute(stmt)
            tags = result.scalars().all()
            return [
                {
                    "id": t.id,
                    "name": t.name,
                    "slug": t.slug,
                    "description": t.description,
                    "sort_order": t.sort_order,
                }
                for t in tags
            ]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    obj = TagDefinition(**data)
                    db.add(obj)
                    await db.flush()
                    await db.refresh(obj)
                    await db.commit()
                    return {
                        "id": obj.id,
                        "name": obj.name,
                        "slug": obj.slug,
                        "description": obj.description,
                        "sort_order": obj.sort_order,
                    }
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class TagRepo(BaseRepository):
                model = TagDefinition

            async with async_session_factory() as db:
                try:
                    result = await TagRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

    @site.register(ServiceDefinition)
    class ServiceAdmin(ModelAdmin):
        list_display = ["id", "name", "slug", "sort_order"]
        search_fields = ["name", "slug"]
        list_per_page = 50

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(ServiceDefinition)
                .where(ServiceDefinition.deleted_at.is_(None))
                .order_by(ServiceDefinition.sort_order)
            )
            result = await db.execute(stmt)
            svcs = result.scalars().all()
            return [
                {
                    "id": s.id,
                    "name": s.name,
                    "slug": s.slug,
                    "description": s.description,
                    "sort_order": s.sort_order,
                }
                for s in svcs
            ]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    obj = ServiceDefinition(**data)
                    db.add(obj)
                    await db.flush()
                    await db.refresh(obj)
                    await db.commit()
                    return {
                        "id": obj.id,
                        "name": obj.name,
                        "slug": obj.slug,
                        "description": obj.description,
                        "sort_order": obj.sort_order,
                    }
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class SvcRepo(BaseRepository):
                model = ServiceDefinition

            async with async_session_factory() as db:
                try:
                    result = await SvcRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

    @site.register(Expert)
    class ExpertAdmin(ModelAdmin):
        list_display = [
            "id", "name", "title", "summary", "is_published",
            "sort_order", "platform_count", "case_count",
        ]
        list_filter = {"is_published": [True, False]}
        search_fields = ["name", "summary"]
        list_per_page = 20

        model_schema_update = ExpertUpdate
        model_schema_response = ExpertDetailResponse

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Expert)
                .options(
                    joinedload(Expert.tags),
                    joinedload(Expert.services),
                    joinedload(Expert.platforms),
                    joinedload(Expert.cases),
                )
                .where(Expert.deleted_at.is_(None))
                .order_by(Expert.sort_order)
            )
            result = await db.execute(stmt)
            experts = result.scalars().unique().all()
            items = []
            for e in experts:
                detail = await get_expert_detail(db, e.id)
                if detail:
                    items.append(detail.model_dump())
            return items

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    expert = await create_expert(db, data)
                    await db.commit()
                    detail = await get_expert_detail(db, expert.id)
                    return detail.model_dump() if detail else {}
                except Exception:
                    await db.rollback()
                    raise

        async def update_object(
            self, id: int, data: dict[str, Any]
        ) -> dict[str, Any] | None:
            async with async_session_factory() as db:
                try:
                    expert = await update_expert(db, id, data)
                    if expert is None:
                        return None
                    await db.commit()
                    detail = await get_expert_detail(db, id)
                    return detail.model_dump() if detail else None
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class ExpertRepo(BaseRepository):
                model = Expert

            async with async_session_factory() as db:
                try:
                    result = await ExpertRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

    @site.register(Platform)
    class PlatformAdmin(ModelAdmin):
        list_display = [
            "id", "expert_id", "platform_type", "platform_name",
            "blogger_name", "sort_order",
        ]
        list_filter = {"platform_type": ["douyin", "xiaohongshu", "wechat_video"]}
        list_per_page = 50

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Platform)
                .where(Platform.deleted_at.is_(None))
                .order_by(Platform.sort_order)
            )
            result = await db.execute(stmt)
            platforms = result.scalars().all()
            return [PlatformResponse.model_validate(p).model_dump() for p in platforms]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    expert_id = data.pop("expert_id", None)
                    if expert_id is None:
                        raise ValueError("expert_id is required")
                    platform = await create_platform(db, int(expert_id), data)
                    await db.commit()
                    return PlatformResponse.model_validate(platform).model_dump()
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            async with async_session_factory() as db:
                try:
                    deleted = await delete_platform(db, id)
                    await db.commit()
                    return deleted
                except Exception:
                    await db.rollback()
                    raise

    @site.register(Case)
    class CaseAdmin(ModelAdmin):
        list_display = ["id", "expert_id", "name", "sort_order"]
        search_fields = ["name"]
        list_per_page = 50

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Case)
                .where(Case.deleted_at.is_(None))
                .order_by(Case.sort_order)
            )
            result = await db.execute(stmt)
            cases = result.scalars().all()
            return [CaseResponse.model_validate(c).model_dump() for c in cases]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    expert_id = data.pop("expert_id", None)
                    if expert_id is None:
                        raise ValueError("expert_id is required")
                    case = await create_case(db, int(expert_id), data)
                    await db.commit()
                    return CaseResponse.model_validate(case).model_dump()
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            async with async_session_factory() as db:
                try:
                    deleted = await delete_case(db, id)
                    await db.commit()
                    return deleted
                except Exception:
                    await db.rollback()
                    raise
