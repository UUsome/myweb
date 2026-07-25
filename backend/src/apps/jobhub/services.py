from __future__ import annotations

from typing import Any

from sqlalchemy import func as sa_func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.jobhub.models import Job
from src.apps.jobhub.schemas import (
    JobDetailResponse,
    JobFilterOptions,
    JobListResponse,
    JobTagSchema,
)
from src.core.logger import get_logger

logger = get_logger(__name__)

AVAILABLE_TAGS: list[dict[str, str]] = [
    {"type": "internal", "label": "内推", "color": "#FF6B6B", "description": "内部推荐职位"},
    {"type": "urgent", "label": "急招", "color": "#FFA94D", "description": "紧急招聘职位"},
    {"type": "expert", "label": "专家推荐", "color": "#4ECDC4", "description": "专家推荐的优质职位"},
]


async def list_jobs(
    db: AsyncSession,
    city: str | None = None,
    industry: str | None = None,
    job_type: str | None = None,
    tag_type: str | None = None,
    keyword: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[JobListResponse], str | None, bool]:
    stmt = (
        select(Job)
        .options(joinedload(Job.contact_expert))
        .where(Job.deleted_at.is_(None), Job.is_active.is_(True))
    )

    if city:
        stmt = stmt.where(Job.city == city)
    if industry:
        stmt = stmt.where(Job.industry == industry)
    if job_type:
        stmt = stmt.where(Job.job_type == job_type)
    if keyword:
        stmt = stmt.where(
            sa_func.lower(Job.title).contains(keyword.lower())
            | sa_func.lower(Job.company_name).contains(keyword.lower())
        )

    if cursor:
        stmt = stmt.where(Job.id < int(cursor))

    # Featured jobs first, then by id desc
    stmt = stmt.order_by(Job.is_featured.desc(), Job.id.desc()).limit(limit + 1)

    result = await db.execute(stmt)
    jobs = list(result.scalars().unique().all())

    has_next = len(jobs) > limit
    if has_next:
        jobs = jobs[:limit]

    next_cursor: str | None = None
    if jobs and has_next:
        next_cursor = str(jobs[-1].id)

    if tag_type:
        jobs = [j for j in jobs if j.tags and any(t.get("type") == tag_type for t in j.tags)]

    items = [
        JobListResponse(
            id=j.id,
            title=j.title,
            company_name=j.company_name,
            company_logo=j.company_logo,
            salary_text=j.salary_text,
            city=j.city,
            industry=j.industry,
            job_type=j.job_type,
            tags=[JobTagSchema(**t) for t in (j.tags or [])],
            is_active=j.is_active,
            is_featured=j.is_featured,
            view_count=j.view_count,
            contact_name=j.contact_name,
            contact_expert_id=j.contact_expert_id,
            created_at=j.created_at,
            updated_at=j.updated_at,
        )
        for j in jobs
    ]

    return items, next_cursor, has_next


async def get_job_detail(db: AsyncSession, job_id: int) -> JobDetailResponse | None:
    stmt = (
        select(Job)
        .options(joinedload(Job.contact_expert))
        .where(Job.id == job_id, Job.deleted_at.is_(None))
    )
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    if job is None:
        return None

    # Increment view count
    job.view_count += 1

    contact_expert_data = None
    if job.contact_expert:
        contact_expert_data = {
            "id": job.contact_expert.id,
            "name": job.contact_expert.name,
            "title": job.contact_expert.title,
            "avatar_url": job.contact_expert.avatar_url,
            "summary": job.contact_expert.summary,
        }

    return JobDetailResponse(
        id=job.id,
        title=job.title,
        company_name=job.company_name,
        company_logo=job.company_logo,
        salary_text=job.salary_text,
        city=job.city,
        industry=job.industry,
        job_type=job.job_type,
        description=job.description,
        requirements=job.requirements,
        benefits=job.benefits,
        tags=[JobTagSchema(**t) for t in (job.tags or [])],
        is_active=job.is_active,
        is_featured=job.is_featured,
        view_count=job.view_count,
        contact_name=job.contact_name,
        contact_expert_id=job.contact_expert_id,
        contact_expert=contact_expert_data,
        expires_at=job.expires_at,
        created_at=job.created_at,
        updated_at=job.updated_at,
    )


async def get_filter_options(db: AsyncSession) -> JobFilterOptions:
    """Get distinct filter values for city, industry, job_type."""
    stmt = select(
        Job.city,
        Job.industry,
        Job.job_type,
    ).where(
        Job.deleted_at.is_(None),
        Job.is_active.is_(True),
    ).distinct()

    result = await db.execute(stmt)
    rows = result.all()

    cities: set[str] = set()
    industries: set[str] = set()
    job_types: set[str] = set()

    for row in rows:
        if row.city:
            cities.add(row.city)
        if row.industry:
            industries.add(row.industry)
        if row.job_type:
            job_types.add(row.job_type)

    return JobFilterOptions(
        cities=sorted(cities),
        industries=sorted(industries),
        job_types=sorted(job_types),
    )


def get_available_tags() -> list[dict[str, str]]:
    """Get available tag definitions."""
    return AVAILABLE_TAGS


async def create_job(db: AsyncSession, data: dict[str, Any]) -> Job:
    tags_data = data.pop("tags", None)
    benefits_data = data.pop("benefits", None)

    job = Job(**data)
    if tags_data:
        job.tags = [t.model_dump() if hasattr(t, "model_dump") else t for t in tags_data]
    if benefits_data:
        job.benefits = benefits_data

    db.add(job)
    await db.flush()
    await db.refresh(job)
    return job


async def update_job(db: AsyncSession, job_id: int, data: dict[str, Any]) -> Job | None:
    stmt = select(Job).where(
        Job.id == job_id,
        Job.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    if job is None:
        return None

    for field, value in data.items():
        setattr(job, field, value)

    await db.flush()
    await db.refresh(job)
    return job


async def toggle_featured(db: AsyncSession, job_id: int) -> Job | None:
    stmt = select(Job).where(
        Job.id == job_id,
        Job.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    if job is None:
        return None
    job.is_featured = not job.is_featured
    await db.flush()
    await db.refresh(job)
    return job
