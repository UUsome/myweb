from __future__ import annotations

from typing import Any

from sqlalchemy import func as sa_func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.apps.experthub.models import (
    Case,
    Expert,
    Platform,
    ServiceDefinition,
    TagDefinition,
    expert_services,
    expert_tags,
)
from src.apps.experthub.schemas import (
    CaseResponse,
    ExpertDetailResponse,
    ExpertHoverResponse,
    ExpertListResponse,
    PlatformResponse,
    ServiceDefinitionResponse,
    TagDefinitionResponse,
)
from src.core.logger import get_logger

logger = get_logger(__name__)


# ── Tag / Service Definition Services ──


async def list_tags(db: AsyncSession) -> list[TagDefinition]:
    stmt = (
        select(TagDefinition)
        .where(TagDefinition.deleted_at.is_(None))
        .order_by(TagDefinition.sort_order)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def list_services(db: AsyncSession) -> list[ServiceDefinition]:
    stmt = (
        select(ServiceDefinition)
        .where(ServiceDefinition.deleted_at.is_(None))
        .order_by(ServiceDefinition.sort_order)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


# ── Expert Services ──


async def list_experts(
    db: AsyncSession,
    tag_slugs: list[str] | None = None,
    service_slugs: list[str] | None = None,
    keyword: str | None = None,
    cursor: str | None = None,
    limit: int = 20,
) -> tuple[list[ExpertListResponse], str | None, bool]:
    stmt = (
        select(Expert)
        .options(
            joinedload(Expert.tags),
            joinedload(Expert.services),
        )
        .where(Expert.deleted_at.is_(None), Expert.is_published.is_(True))
    )

    if tag_slugs:
        stmt = stmt.where(
            Expert.tags.any(TagDefinition.slug.in_(tag_slugs))
        )

    if service_slugs:
        stmt = stmt.where(
            Expert.services.any(ServiceDefinition.slug.in_(service_slugs))
        )

    if keyword:
        stmt = stmt.where(
            sa_func.lower(Expert.name).contains(keyword.lower())
            | sa_func.lower(Expert.summary).contains(keyword.lower())
        )

    if cursor:
        stmt = stmt.where(Expert.id < int(cursor))

    stmt = stmt.order_by(Expert.sort_order, Expert.id.desc()).limit(limit + 1)

    result = await db.execute(stmt)
    experts = list(result.scalars().unique().all())

    has_next = len(experts) > limit
    if has_next:
        experts = experts[:limit]

    next_cursor: str | None = None
    if experts and has_next:
        next_cursor = str(experts[-1].id)

    items = [
        ExpertListResponse(
            id=e.id,
            name=e.name,
            title=e.title,
            summary=e.summary,
            avatar_url=e.avatar_url,
            platform_count=e.platform_count,
            case_count=e.case_count,
            is_published=e.is_published,
            sort_order=e.sort_order,
            created_at=e.created_at,
            updated_at=e.updated_at,
            tags=[TagDefinitionResponse.model_validate(t) for t in (e.tags or [])],
            services=[ServiceDefinitionResponse.model_validate(s) for s in (e.services or [])],
        )
        for e in experts
    ]

    return items, next_cursor, has_next


async def get_expert_detail(db: AsyncSession, expert_id: int) -> ExpertDetailResponse | None:
    stmt = (
        select(Expert)
        .options(
            joinedload(Expert.tags),
            joinedload(Expert.services),
            joinedload(Expert.platforms),
            joinedload(Expert.cases),
        )
        .where(Expert.id == expert_id, Expert.deleted_at.is_(None))
    )
    result = await db.execute(stmt)
    expert = result.unique().scalar_one_or_none()
    if expert is None:
        return None

    return ExpertDetailResponse(
        id=expert.id,
        name=expert.name,
        title=expert.title,
        summary=expert.summary,
        avatar_url=expert.avatar_url,
        contact_email=expert.contact_email,
        contact_phone=expert.contact_phone,
        contact_wechat=expert.contact_wechat,
        platform_count=expert.platform_count,
        case_count=expert.case_count,
        is_published=expert.is_published,
        sort_order=expert.sort_order,
        created_at=expert.created_at,
        updated_at=expert.updated_at,
        tags=[TagDefinitionResponse.model_validate(t) for t in (expert.tags or [])],
        services=[ServiceDefinitionResponse.model_validate(s) for s in (expert.services or [])],
        platforms=[PlatformResponse.model_validate(p) for p in (expert.platforms or [])],
        cases=[CaseResponse.model_validate(c) for c in (expert.cases or [])],
    )


async def get_expert_hover(db: AsyncSession, expert_id: int) -> ExpertHoverResponse | None:
    """Get hover card data (summary + first few platforms/cases)."""
    stmt = (
        select(Expert)
        .options(
            joinedload(Expert.tags),
            joinedload(Expert.platforms),
            joinedload(Expert.cases),
        )
        .where(Expert.id == expert_id, Expert.deleted_at.is_(None))
    )
    result = await db.execute(stmt)
    expert = result.unique().scalar_one_or_none()
    if expert is None:
        return None

    return ExpertHoverResponse(
        id=expert.id,
        name=expert.name,
        title=expert.title,
        summary=expert.summary,
        avatar_url=expert.avatar_url,
        platform_count=expert.platform_count,
        case_count=expert.case_count,
        platforms=[PlatformResponse.model_validate(p) for p in (expert.platforms or [])[:3]],
        cases=[CaseResponse.model_validate(c) for c in (expert.cases or [])[:3]],
        tags=[TagDefinitionResponse.model_validate(t) for t in (expert.tags or [])],
    )


async def create_expert(db: AsyncSession, data: dict[str, Any]) -> Expert:
    tag_ids = data.pop("tag_ids", [])
    service_ids = data.pop("service_ids", [])

    expert = Expert(**data)
    db.add(expert)
    await db.flush()

    # Set tags and services
    if tag_ids:
        tag_stmt = select(TagDefinition).where(TagDefinition.id.in_(tag_ids))
        tag_result = await db.execute(tag_stmt)
        expert.tags = list(tag_result.scalars().all())

    if service_ids:
        svc_stmt = select(ServiceDefinition).where(ServiceDefinition.id.in_(service_ids))
        svc_result = await db.execute(svc_stmt)
        expert.services = list(svc_result.scalars().all())

    await db.flush()
    await db.refresh(expert)
    return expert


async def update_expert(db: AsyncSession, expert_id: int, data: dict[str, Any]) -> Expert | None:
    stmt = select(Expert).where(
        Expert.id == expert_id,
        Expert.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    expert = result.unique().scalar_one_or_none()
    if expert is None:
        return None

    tag_ids = data.pop("tag_ids", None)
    service_ids = data.pop("service_ids", None)

    for field, value in data.items():
        setattr(expert, field, value)

    if tag_ids is not None:
        tag_stmt = select(TagDefinition).where(TagDefinition.id.in_(tag_ids))
        tag_result = await db.execute(tag_stmt)
        expert.tags = list(tag_result.scalars().all())

    if service_ids is not None:
        svc_stmt = select(ServiceDefinition).where(ServiceDefinition.id.in_(service_ids))
        svc_result = await db.execute(svc_stmt)
        expert.services = list(svc_result.scalars().all())

    await db.flush()
    await db.refresh(expert)
    return expert


# ── Platform Services ──


async def get_expert_platforms(
    db: AsyncSession, expert_id: int
) -> list[Platform]:
    stmt = (
        select(Platform)
        .where(
            Platform.expert_id == expert_id,
            Platform.deleted_at.is_(None),
        )
        .order_by(Platform.sort_order)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_platform(db: AsyncSession, expert_id: int, data: dict[str, Any]) -> Platform:
    platform = Platform(expert_id=expert_id, **data)
    db.add(platform)
    await db.flush()
    await db.refresh(platform)

    # Update expert platform_count
    stmt = select(Expert).where(Expert.id == expert_id)
    result = await db.execute(stmt)
    expert = result.unique().scalar_one_or_none()
    if expert:
        count_stmt = select(sa_func.count()).select_from(Platform).where(
            Platform.expert_id == expert_id,
            Platform.deleted_at.is_(None),
        )
        count_result = await db.execute(count_stmt)
        expert.platform_count = count_result.scalar_one()

    return platform


async def update_platform(
    db: AsyncSession, platform_id: int, data: dict[str, Any]
) -> Platform | None:
    stmt = select(Platform).where(
        Platform.id == platform_id,
        Platform.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    platform = result.scalar_one_or_none()
    if platform is None:
        return None
    for field, value in data.items():
        setattr(platform, field, value)
    await db.flush()
    await db.refresh(platform)
    return platform


async def delete_platform(db: AsyncSession, platform_id: int) -> bool:
    from src.apps.core.base_repository import BaseRepository

    class PlatformRepo(BaseRepository):
        model = Platform

    platform = await PlatformRepo.get_by_id(db, platform_id)
    if platform is None:
        return False

    expert_id = platform.expert_id
    result = await PlatformRepo.soft_delete(db, platform_id)

    # Update expert platform_count
    if result:
        stmt = select(Expert).where(Expert.id == expert_id)
        r = await db.execute(stmt)
        expert = r.scalar_one_or_none()
        if expert:
            count_stmt = select(sa_func.count()).select_from(Platform).where(
                Platform.expert_id == expert_id,
                Platform.deleted_at.is_(None),
            )
            count_result = await db.execute(count_stmt)
            expert.platform_count = count_result.scalar_one()

    return result is not None


# ── Case Services ──


async def get_expert_cases(
    db: AsyncSession, expert_id: int
) -> list[Case]:
    stmt = (
        select(Case)
        .where(
            Case.expert_id == expert_id,
            Case.deleted_at.is_(None),
        )
        .order_by(Case.sort_order)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_case_detail(db: AsyncSession, case_id: int) -> Case | None:
    stmt = select(Case).where(
        Case.id == case_id,
        Case.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_case(db: AsyncSession, expert_id: int, data: dict[str, Any]) -> Case:
    case = Case(expert_id=expert_id, **data)
    db.add(case)
    await db.flush()
    await db.refresh(case)

    # Update expert case_count
    stmt = select(Expert).where(Expert.id == expert_id)
    result = await db.execute(stmt)
    expert = result.unique().scalar_one_or_none()
    if expert:
        count_stmt = select(sa_func.count()).select_from(Case).where(
            Case.expert_id == expert_id,
            Case.deleted_at.is_(None),
        )
        count_result = await db.execute(count_stmt)
        expert.case_count = count_result.scalar_one()

    return case


async def update_case(
    db: AsyncSession, case_id: int, data: dict[str, Any]
) -> Case | None:
    stmt = select(Case).where(
        Case.id == case_id,
        Case.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    case = result.scalar_one_or_none()
    if case is None:
        return None
    for field, value in data.items():
        setattr(case, field, value)
    await db.flush()
    await db.refresh(case)
    return case


async def delete_case(db: AsyncSession, case_id: int) -> bool:
    from src.apps.core.base_repository import BaseRepository

    class CaseRepo(BaseRepository):
        model = Case

    case = await CaseRepo.get_by_id(db, case_id)
    if case is None:
        return False

    expert_id = case.expert_id
    result = await CaseRepo.soft_delete(db, case_id)

    if result:
        stmt = select(Expert).where(Expert.id == expert_id)
        r = await db.execute(stmt)
        expert = r.scalar_one_or_none()
        if expert:
            count_stmt = select(sa_func.count()).select_from(Case).where(
                Case.expert_id == expert_id,
                Case.deleted_at.is_(None),
            )
            count_result = await db.execute(count_stmt)
            expert.case_count = count_result.scalar_one()

    return result is not None
