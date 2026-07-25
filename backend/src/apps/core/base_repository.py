from __future__ import annotations

from datetime import datetime, timezone
from typing import Generic, TypeVar

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.core.base_model import CoreModel

ModelT = TypeVar("ModelT", bound=CoreModel)


class BaseRepository(Generic[ModelT]):
    """Generic CRUD repository with soft-delete support."""

    model: type[ModelT] | None = None

    @classmethod
    async def get_active(
        cls, db: AsyncSession, id: int
    ) -> ModelT | None:
        """Query a record that is not soft-deleted."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        stmt = select(cls.model).where(
            cls.model.id == id,  # type: ignore[attr-defined]
            cls.model.deleted_at.is_(None),  # type: ignore[attr-defined]
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_by_id(
        cls, db: AsyncSession, id: int, include_deleted: bool = False
    ) -> ModelT | None:
        """Query a record by ID, optionally including soft-deleted."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        stmt = select(cls.model).where(cls.model.id == id)  # type: ignore[attr-defined]
        if not include_deleted:
            stmt = stmt.where(cls.model.deleted_at.is_(None))  # type: ignore[attr-defined]
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def list_active(
        cls, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelT]:
        """List records excluding soft-deleted ones."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        stmt = (
            select(cls.model)
            .where(cls.model.deleted_at.is_(None))  # type: ignore[attr-defined]
            .offset(skip)
            .limit(limit)
            .order_by(cls.model.id)  # type: ignore[attr-defined]
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    @classmethod
    async def count_active(cls, db: AsyncSession) -> int:
        """Count records excluding soft-deleted ones."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        from sqlalchemy import func as sa_func

        stmt = select(sa_func.count()).select_from(cls.model).where(
            cls.model.deleted_at.is_(None)  # type: ignore[attr-defined]
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs) -> ModelT:
        """Create a new record."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        instance = cls.model(**kwargs)
        db.add(instance)
        await db.flush()
        await db.refresh(instance)
        return instance

    @classmethod
    async def update(
        cls, db: AsyncSession, id: int, **kwargs
    ) -> ModelT | None:
        """Update a record by ID."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        stmt = (
            update(cls.model)
            .where(cls.model.id == id)  # type: ignore[attr-defined]
            .where(cls.model.deleted_at.is_(None))  # type: ignore[attr-defined]
            .values(**kwargs)
            .returning(cls.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def soft_delete(cls, db: AsyncSession, id: int) -> ModelT | None:
        """Soft-delete a record by ID."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        stmt = (
            update(cls.model)
            .where(cls.model.id == id)  # type: ignore[attr-defined]
            .where(cls.model.deleted_at.is_(None))  # type: ignore[attr-defined]
            .values(deleted_at=datetime.now(timezone.utc))
            .returning(cls.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def restore(cls, db: AsyncSession, id: int) -> ModelT | None:
        """Restore a soft-deleted record."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        stmt = (
            update(cls.model)
            .where(cls.model.id == id)  # type: ignore[attr-defined]
            .values(deleted_at=None)
            .returning(cls.model)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def exists(cls, db: AsyncSession, id: int) -> bool:
        """Check if a record exists and is not soft-deleted."""
        if cls.model is None:
            raise NotImplementedError("model class must be defined")
        stmt = select(cls.model.id).where(  # type: ignore[attr-defined]
            cls.model.id == id,  # type: ignore[attr-defined]
            cls.model.deleted_at.is_(None),  # type: ignore[attr-defined]
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none() is not None
