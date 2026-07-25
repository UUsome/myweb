from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.admin.site import AdminSite, ModelAdmin
from src.apps.jobhub.models import Job
from src.apps.jobhub.schemas import JobDetailResponse, JobUpdate
from src.apps.jobhub.services import (
    create_job,
    get_job_detail,
    toggle_featured,
    update_job,
)
from src.core.database import async_session_factory
from src.core.logger import get_logger

logger = get_logger(__name__)


def register_admin(site: AdminSite) -> None:
    @site.register(Job)
    class JobAdmin(ModelAdmin):
        list_display = [
            "id", "title", "company_name", "city", "industry",
            "job_type", "is_active", "is_featured", "view_count", "created_at",
        ]
        list_filter = {
            "city": [],
            "industry": [],
            "job_type": ["全职", "兼职", "实习"],
            "is_active": [True, False],
            "is_featured": [True, False],
        }
        search_fields = ["title", "company_name", "description"]
        list_per_page = 20

        model_schema_create = None  # Will use dict
        model_schema_update = JobUpdate
        model_schema_response = JobDetailResponse

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = (
                select(Job)
                .options(joinedload(Job.contact_expert))
                .where(Job.deleted_at.is_(None))
                .order_by(Job.is_featured.desc(), Job.id.desc())
            )
            result = await db.execute(stmt)
            jobs = result.scalars().unique().all()
            items = []
            for j in jobs:
                detail = await get_job_detail(db, j.id)
                if detail:
                    items.append(detail.model_dump())
            return items

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    job = await create_job(db, data)
                    await db.commit()
                    detail = await get_job_detail(db, job.id)
                    return detail.model_dump() if detail else {}
                except Exception:
                    await db.rollback()
                    raise

        async def update_object(
            self, id: int, data: dict[str, Any]
        ) -> dict[str, Any] | None:
            async with async_session_factory() as db:
                try:
                    job = await update_job(db, id, data)
                    if job is None:
                        return None
                    await db.commit()
                    detail = await get_job_detail(db, id)
                    return detail.model_dump() if detail else None
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            from src.apps.core.base_repository import BaseRepository

            class JobRepo(BaseRepository):
                model = Job

            async with async_session_factory() as db:
                try:
                    result = await JobRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

        async def toggle_featured_action(self, id: int) -> dict[str, Any] | None:
            async with async_session_factory() as db:
                try:
                    job = await toggle_featured(db, id)
                    if job is None:
                        return None
                    await db.commit()
                    detail = await get_job_detail(db, id)
                    return detail.model_dump() if detail else None
                except Exception:
                    await db.rollback()
                    raise
