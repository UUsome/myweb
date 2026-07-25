from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.core.response import APIResponse, success
from src.apps.users import services as user_services
from src.apps.users.dependencies import get_current_user
from src.apps.users.models import User, UserRole
from src.apps.users.schemas import (
    LoginRequest,
    RefreshRequest,
    TokenResponse,
    UserPublicResponse,
    UserResponse,
    UserUpdate,
)
from src.core.database import get_db
from src.core.logger import get_logger

from .exceptions import BadRequest, Forbidden, NotImplemented as NotImplemented_

logger = get_logger(__name__)

router = APIRouter(tags=["Users"])


@router.post(
    "/auth/login",
    summary="用户登录",
    description="用户使用用户名和密码登录，返回 JWT access_token 和 refresh_token",

)
async def login(
    req: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[TokenResponse]:
    user = await user_services.authenticate_user(db, req.username, req.password)
    if user is None:
        raise BadRequest(message="用户名或密码错误")

    if user.is_frozen:
        raise Forbidden(message="账号已被冻结")

    access_token = user_services.create_access_token(user.id, user.role)
    refresh_token = user_services.create_refresh_token(user.id)
    await user_services.store_refresh_token(user.id, refresh_token)

    return success(
        data=TokenResponse(access_token=access_token, refresh_token=refresh_token)
    )


@router.post(
    "/auth/refresh",
    summary="刷新 Token",
    description="使用 refresh_token 获取新的 access_token",
)
async def refresh_token(
    req: RefreshRequest,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[TokenResponse]:
    try:
        payload = user_services.decode_token(req.refresh_token)
        if payload.get("type") != "refresh":
            raise BadRequest(message="无效的 refresh_token")
    except Exception:
        raise BadRequest(message="无效的 refresh_token")

    user_id = int(payload.get("sub", "0"))
    if user_id <= 0:
        raise BadRequest(message="无效的 refresh_token")

    valid = await user_services.validate_refresh_token(user_id, req.refresh_token)
    if not valid:
        raise BadRequest(message="refresh_token 已失效")

    stmt = select(User).where(User.id == user_id, User.deleted_at.is_(None))
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise BadRequest(message="用户不存在")

    access_token = user_services.create_access_token(user.id, user.role.value)
    refresh_token = user_services.create_refresh_token(user.id)
    await user_services.store_refresh_token(user.id, refresh_token)

    return success(
        data=TokenResponse(access_token=access_token, refresh_token=refresh_token)
    )


@router.post(
    "/auth/logout",
    summary="退出登录",
    description="使当前用户的 refresh_token 失效",
)
async def logout(
    current_user: User = Depends(get_current_user),
) -> APIResponse[None]:
    await user_services.remove_refresh_token(current_user.id)
    return success(message="已退出登录")


@router.get(
    "/users/me",
    summary="获取当前用户信息",
    description="获取已登录用户的详细信息",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> APIResponse[UserResponse]:
    return success(data=UserResponse.model_validate(current_user))


@router.put(
    "/users/me",
    summary="更新当前用户信息",
    description="更新已登录用户的基本信息",
)
async def update_me(
    req: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> APIResponse[UserResponse]:
    update_data = req.model_dump(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(current_user, field, value)
        await db.flush()
        await db.refresh(current_user)

    return success(data=UserResponse.model_validate(current_user))


@router.get(
    "/users/{user_id}",
    summary="获取用户信息",
    description="公开接口，获取任意用户的基本公开信息",
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> APIResponse[UserPublicResponse]:
    user = await user_services.get_user_by_id(db, user_id)
    if user is None:
        from .exceptions import NotFound

        raise NotFound(message="用户不存在")

    return success(data=UserPublicResponse.model_validate(user))


# ── 保留接口：注册 ──


@router.post("/auth/register", summary="用户注册", description="暂不开发")
async def register() -> APIResponse[None]:
    raise NotImplemented_(message="用户注册功能开发中")


@router.post("/auth/verify-email", summary="邮箱验证", description="暂不开发")
async def verify_email() -> APIResponse[None]:
    raise NotImplemented_(message="邮箱验证功能开发中")


@router.post("/auth/verify-phone", summary="手机验证", description="暂不开发")
async def verify_phone() -> APIResponse[None]:
    raise NotImplemented_(message="手机验证功能开发中")
