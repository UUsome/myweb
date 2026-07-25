from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.core.pagination import CursorPage
from src.apps.core.response import APIResponse, success
from src.apps.jobhub import services as job_services
from src.apps.jobhub.schemas import (
    JobCreate,
    JobDetailResponse,
    JobFilterOptions,
    JobListResponse,
    JobTagAvailable,
    JobUpdate,
)
from src.apps.users.dependencies import get_current_admin_user
from src.apps.users.models import User
from src.core.database import get_db
from src.core.logger import get_logger

from .exceptions import NotFound

logger = get_logger(__name__)

router = APIRouter(tags=["JobHub"])


@router.get(
    "/jobs",
    summary="职位列表",
    description="职位列表，支持城市/行业/类型/标签筛+ 游标分页",
)
async def list_jobs(
    city: str | None = Query(None, description="城市"),
    industry: str | None = Query(None, description="行业"),
    job_type: str | None = Query(None, description="职位类型"),
    tag_type: str | None = Query(None, description="标签类型 (internal/urgent/expert)"),
    keyword: str | None = Query(None, description="关键词搜"),
    cursor: str | None = Query(None, description="游标"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[CursorPage[JobListResponse]]:
    items, next_cursor, has_next = await job_services.list_jobs(
        db, city, industry, job_type, tag_type, keyword, cursor, limit
    )
    return success(data=CursorPage(list=items, cursor=next_cursor, has_next=has_next))


@router.get(
    "/jobs/{job_id}",
    summary="职位详情",
    description="获取职位详细信息（含联系人专家信+ 浏览）",
)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[JobDetailResponse]:
    job = await job_services.get_job_detail(db, job_id)
    if job is None:
        raise NotFound(message="职位不存")
    return success(data=job)


@router.get(
    "/jobs/filters/options",
    summary="获取筛选选项",
    description="获取职位筛选的城市/行业/类型选项",
)
async def get_filter_options(
    db: AsyncSession = Depends(get_db),
) -> APIResponse[JobFilterOptions]:
    options = await job_services.get_filter_options(db)
    return success(data=options)


@router.get(
    "/jobs/tags/available",
    summary="获取可用标签定义",
    description="获取可用的职位标签定义列",
)
async def get_available_tags() -> APIResponse[list[JobTagAvailable]]:
    tags = job_services.get_available_tags()
    return success(data=[JobTagAvailable(**t) for t in tags])


# ── Admin CRUD ──


@router.post(
    "/jobs",
    summary="创建职位",
    description="创建新职位（管理员）",
)
async def create_job(
    req: JobCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[JobDetailResponse]:
    job = await job_services.create_job(db, req.model_dump())
    detail = await job_services.get_job_detail(db, job.id)
    return success(data=detail, message="职位创建成功")


@router.put(
    "/jobs/{job_id}",
    summary="更新职位",
    description="更新职位信息（管理员",
)
async def update_job(
    job_id: int,
    req: JobUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[JobDetailResponse]:
    job = await job_services.update_job(db, job_id, req.model_dump(exclude_unset=True))
    if job is None:
        raise NotFound(message="职位不存")
    detail = await job_services.get_job_detail(db, job_id)
    return success(data=detail, message="职位更新成功")


@router.delete(
    "/jobs/{job_id}",
    summary="删除职位",
    description="删除职位（管理员，软删除",
)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[None]:
    from src.apps.core.base_repository import BaseRepository
    from src.apps.jobhub.models import Job as JobModel

    class JobRepo(BaseRepository):
        model = JobModel

    result = await JobRepo.soft_delete(db, job_id)
    if result is None:
        raise NotFound(message="职位不存")
    return success(message="职位删除成功")


@router.post(
    "/jobs/{job_id}/toggle-featured",
    summary="切换置顶状",
    description="切换职位置顶/取消置顶状态（管理员）",
)
async def toggle_featured(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
) -> APIResponse[JobDetailResponse]:
    job = await job_services.toggle_featured(db, job_id)
    if job is None:
        raise NotFound(message="职位不存")
    detail = await job_services.get_job_detail(db, job_id)
    return success(data=detail, message="置顶状态已切换")
