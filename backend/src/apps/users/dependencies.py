from __future__ import annotations

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.models import User, UserRole
from src.apps.users.services import decode_token
from src.core.database import get_db
from src.core.logger import get_logger

from .exceptions import Forbidden, TokenExpired, Unauthorized

logger = get_logger(__name__)


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extract and validate current user from JWT token in Authorization header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise Unauthorized()

    token = auth_header.removeprefix("Bearer ")

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise Unauthorized()
    except Exception:
        raise TokenExpired()

    user_id = int(payload.get("sub", "0"))
    if user_id <= 0:
        raise Unauthorized()

    from .services import get_user_by_id

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise Unauthorized()

    if user.is_frozen:
        raise Forbidden(message="账号已被冻结")

    request.state.current_user = user
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure the current user is an admin."""
    if current_user.role != UserRole.ADMIN:
        raise Forbidden(message="需要管理员权限")
    return current_user
