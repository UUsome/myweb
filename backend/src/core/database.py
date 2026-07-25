from __future__ import annotations

from sqlalchemy import event as sa_event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

# ── 数据库────────────────────────────────
# SQLite 不使用连接池，其余数据库使用连接字符串
_engine_kwargs: dict = {
    "echo": settings.is_dev,
}

if not settings.is_sqlite:
    _engine_kwargs["pool_size"] = 10
    _engine_kwargs["max_overflow"] = 20
    _engine_kwargs["pool_pre_ping"] = True
else:
    # SQLite 需check_same_thread=False
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(
    settings.database_url_async,
    **_engine_kwargs,
)

# SQLite 事件：每次连接时启用外键约束
if settings.is_sqlite:

    @sa_event.listens_for(engine.sync_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # type: ignore[misc]
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:  # type: ignore[misc]
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Create all tables (for dev/test use; prod should use Alembic)."""
    async with engine.begin() as conn:
        # Import all models here to ensure they're registered on Base.metadata
        import src.apps.users.models  # noqa: F401
        import src.apps.forum.models  # noqa: F401
        import src.apps.interactions.models  # noqa: F401
        import src.apps.experthub.models  # noqa: F401
        import src.apps.jobhub.models  # noqa: F401

        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()
