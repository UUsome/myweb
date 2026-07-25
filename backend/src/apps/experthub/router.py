from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.core.pagination import CursorPage
from src.apps.core.response import APIResponse, success
from src.apps.experthub import services as expert_services
from src.apps.experthub.schemas import (
    CaseBase,
    CaseResponse,
    ExpertCreate,
    ExpertDetailResponse,
    ExpertHoverResponse,
    ExpertListResponse,
    ExpertUpdate,
    PlatformBase,
    PlatformResponse,
    ServiceDefinitionResponse,
    TagDefinitionResponse,
)
from src.apps.users.dependencies import get_current_admin_user
from src.apps.users.models import User
from src.core.database import get_db
from src.core.logger import get_logger

from .exceptions import NotFound

logger = get_logger(__name__)

router = APIRouter(tags=["ExpertHub"])


# ── Tags & Services ──


@router.get(
    "/tags",
    summary="获取所有标",
    description="获取所有专家标签定",
)
async def get_tags(
    db: AsyncSession = Depends(get_db),
) -> APIResponse[list[TagDefinitionResponse]]:
    tags = await expert_services.list_tags(db)
    return success(data=[TagDefinitionResponse.model_validate(t) for t in tags])


@router.get(
    "/services",
    summary="获取所有服务形",
    description="获取所有专家服务形式定",
)
async def get_services(
    db: AsyncSession = Depends(get_db),
) -> APIResponse[list[ServiceDefinitionResponse]]:
    services = await expert_services.list_services(db)
    return success(data=[ServiceDefinitionResponse.model_validate(s) for s in services])


# ── Experts ──


@router.get(
    "/experts",
    summary="专家列表",
    description="专家列表，支持服务/关键词筛+ 游标分页",
)
async def list_experts(
    tag: list[str] = Query(default=[], description="标签 slug 筛"),
    service: list[str] = Query(default=[], description="服务 slug 筛"),
    keyword: str | None = Query(None, description="关键词搜"),
    cursor: str | None = Query(None, description="游标"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[CursorPage[ExpertListResponse]]:
    tag_list = tag if tag else None
    service_list = service if service else None
    items, next_cursor, has_next = await expert_services.list_experts(
        db, tag_list, service_list, keyword, cursor, limit
    )
    return success(data=CursorPage(list=items, cursor=next_cursor, has_next=has_next))


@router.get(
    "/experts/{expert_id}",
    summary="专家详情",
    description="获取专家详细信息（含平台/案例)",
)
async def get_expert(
    expert_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[ExpertDetailResponse]:
    expert = await expert_services.get_expert_detail(db, expert_id)
    if expert is None:
        raise NotFound(message="专家不存")
    return success(data=expert)


@router.get(
    "/experts/{expert_id}/hover",
    summary="Hover 浮层数据",
    description="获取专家Hover 浮层摘要数据",
)
async def get_expert_hover(
    expert_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[ExpertHoverResponse]:
    hover = await expert_services.get_expert_hover(db, expert_id)
    if hover is None:
        raise NotFound(message="专家不存")
    return success(data=hover)


@router.get(
    "/experts/{expert_id}/platforms",
    summary="专家平台列表",
    description="获取专家的入驻平台列",
)
async def get_expert_platforms(
    expert_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[list[PlatformResponse]]:
    platforms = await expert_services.get_expert_platforms(db, expert_id)
    return success(data=[PlatformResponse.model_validate(p) for p in platforms])


@router.get(
    "/experts/{expert_id}/cases",
    summary="专家案例列表",
    description="获取专家的案例列",
)
async def get_expert_cases(
    expert_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[list[CaseResponse]]:
    cases = await expert_services.get_expert_cases(db, expert_id)
    return success(data=[CaseResponse.model_validate(c) for c in cases])


@router.get(
    "/experts/cases/{case_id}",
    summary="案例详情",
    description="获取专家案例的详细信",
)
async def get_case_detail(
    case_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[CaseResponse]:
    case = await expert_services.get_case_detail(db, case_id)
    if case is None:
        raise NotFound(message="案例不存")
    return success(data=CaseResponse.model_validate(case))


# ── Admin: Expert CRUD ──


@router.post(
    "/experts",
    summary="创建专家",
    description="创建新的专家卡片（管理员",
)
async def create_expert(
    req: ExpertCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[ExpertDetailResponse]:
    expert = await expert_services.create_expert(db, req.model_dump())
    detail = await expert_services.get_expert_detail(db, expert.id)
    return success(data=detail, message="专家创建成功")


@router.put(
    "/experts/{expert_id}",
    summary="更新专家",
    description="更新专家卡片信息（管理员",
)
async def update_expert(
    expert_id: int,
    req: ExpertUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[ExpertDetailResponse]:
    expert = await expert_services.update_expert(db, expert_id, req.model_dump(exclude_unset=True))
    if expert is None:
        raise NotFound(message="专家不存")
    detail = await expert_services.get_expert_detail(db, expert_id)
    return success(data=detail, message="专家更新成功")


@router.delete(
    "/experts/{expert_id}",
    summary="删除专家",
    description="删除专家卡片（管理员，软删除",
)
async def delete_expert(
    expert_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[None]:
    from src.apps.core.base_repository import BaseRepository
    from src.apps.experthub.models import Expert as ExpertModel

    class ExpertRepo(BaseRepository):
        model = ExpertModel

    result = await ExpertRepo.soft_delete(db, expert_id)
    if result is None:
        raise NotFound(message="专家不存")
    return success(message="专家删除成功")


# ── Admin: Platform CRUD ──


@router.post(
    "/experts/{expert_id}/platforms",
    summary="添加平台",
    description="为专家添加入驻平台（管理员）",
)
async def create_platform(
    expert_id: int,
    req: PlatformBase,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[PlatformResponse]:
    platform = await expert_services.create_platform(db, expert_id, req.model_dump())
    return success(data=PlatformResponse.model_validate(platform), message="平台添加成功")


@router.put(
    "/platforms/{platform_id}",
    summary="更新平台",
    description="更新专家平台信息（管理员",
)
async def update_platform(
    platform_id: int,
    req: PlatformBase,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[PlatformResponse]:
    platform = await expert_services.update_platform(db, platform_id, req.model_dump(exclude_unset=True))
    if platform is None:
        raise NotFound(message="平台不存")
    return success(data=PlatformResponse.model_validate(platform), message="平台更新成功")


@router.delete(
    "/platforms/{platform_id}",
    summary="删除平台",
    description="删除专家平台（管理员",
)
async def delete_platform(
    platform_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[None]:
    deleted = await expert_services.delete_platform(db, platform_id)
    if not deleted:
        raise NotFound(message="平台不存")
    return success(message="平台删除成功")


# ── Admin: Case CRUD ──


@router.post(
    "/experts/{expert_id}/cases",
    summary="添加案例",
    description="为专家添加案例（管理员）",
)
async def create_case(
    expert_id: int,
    req: CaseBase,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[CaseResponse]:
    case = await expert_services.create_case(db, expert_id, req.model_dump())
    return success(data=CaseResponse.model_validate(case), message="案例添加成功")


@router.put(
    "/cases/{case_id}",
    summary="更新案例",
    description="更新专家案例信息（管理员",
)
async def update_case(
    case_id: int,
    req: CaseBase,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[CaseResponse]:
    case = await expert_services.update_case(db, case_id, req.model_dump(exclude_unset=True))
    if case is None:
        raise NotFound(message="案例不存")
    return success(data=CaseResponse.model_validate(case), message="案例更新成功")


@router.delete(
    "/cases/{case_id}",
    summary="删除案例",
    description="删除专家案例（管理员",
)
async def delete_case(
    case_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[None]:
    deleted = await expert_services.delete_case(db, case_id)
    if not deleted:
        raise NotFound(message="案例不存")
    return success(message="案例删除成功")
