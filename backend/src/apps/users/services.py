from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.users.models import User
from src.apps.users.schemas import UserCreate
from src.core.config import settings
from src.core.logger import get_logger

if TYPE_CHECKING:
    from redis.asyncio import Redis as RedisType

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: int, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {
        "sub": str(user_id),
        "role": role,
        "type": "access",
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict:
    """Decode JWT token. Raises JWTError if invalid/expired."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])


# ── 内存存储（Redis 不可用时兜底）──────────────
_token_store: dict[str, str] = {}  # key=refresh_token:user_id, value=token
_redis_available: bool | None = None


def _check_redis() -> bool:
    """检查 Redis 是否可用（惰性检测，缓存结果）。"""
    global _redis_available
    if _redis_available is not None:
        return _redis_available
    if settings.has_redis:
        try:
            from redis.asyncio import Redis as RedisType

            _redis_available = True
        except ImportError:
            logger.warning("redis 包未安装，使用内存存储 refresh token")
            _redis_available = False
    else:
        _redis_available = False
    return _redis_available


async def _get_redis() -> "RedisType | None":
    """获取 Redis 连接，不可用时返回 None。"""
    if not _check_redis():
        return None
    from redis.asyncio import Redis as RedisType

    try:
        return RedisType.from_url(  # type: ignore[call-arg]
            settings.REDIS_URL, decode_responses=True  # type: ignore[arg-type]
        )
    except Exception as e:
        logger.warning(f"Redis 连接失败，使用内存存储: {e}")
        return None


async def store_refresh_token(user_id: int, refresh_token: str) -> None:
    redis = await _get_redis()
    if redis is not None:
        key = f"refresh_token:{user_id}"
        await redis.setex(key, settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 86400, refresh_token)
        await redis.aclose()
    else:
        # 内存兜底
        _token_store[f"refresh_token:{user_id}"] = refresh_token
        logger.debug(f"Refresh token stored in memory for user {user_id}")


async def validate_refresh_token(user_id: int, refresh_token: str) -> bool:
    redis = await _get_redis()
    if redis is not None:
        key = f"refresh_token:{user_id}"
        stored = await redis.get(key)
        await redis.aclose()
        return stored == refresh_token
    else:
        stored = _token_store.get(f"refresh_token:{user_id}")
        return stored == refresh_token


async def remove_refresh_token(user_id: int) -> None:
    redis = await _get_redis()
    if redis is not None:
        key = f"refresh_token:{user_id}"
        await redis.delete(key)
        await redis.aclose()
    else:
        _token_store.pop(f"refresh_token:{user_id}", None)


async def authenticate_user(
    db: AsyncSession, username: str, password: str
) -> User | None:
    """Authenticate a user by username and password."""
    stmt = select(User).where(
        User.username == username,
        User.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    """Create a new user (admin only)."""
    from src.apps.users.models import UserRole, UserStatus

    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        nickname=user_data.nickname,
        avatar_url=user_data.avatar_url,
        role=user_data.role or UserRole.MEMBER,
        status=user_data.status or UserStatus.ACTIVE,
        phone=user_data.phone,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(
        User.id == user_id,
        User.deleted_at.is_(None),
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()