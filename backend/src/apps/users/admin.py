from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.admin.site import AdminSite, ModelAdmin
from src.apps.users.models import User
from src.apps.users.schemas import UserCreate, UserResponse, UserUpdateAdmin
from src.apps.users.services import create_user, hash_password
from src.core.database import async_session_factory
from src.core.logger import get_logger

logger = get_logger(__name__)


def register_admin(site: AdminSite) -> None:
    @site.register(User)
    class UserAdmin(ModelAdmin):
        list_display = ["id", "username", "email", "nickname", "role", "status", "created_at"]
        list_filter = {
            "role": ["admin", "moderator", "member"],
            "status": ["active", "frozen"],
        }
        search_fields = ["username", "email"]
        list_per_page = 20

        model_schema_create = UserCreate
        model_schema_update = UserUpdateAdmin
        model_schema_response = UserResponse

        async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
            stmt = select(User).where(User.deleted_at.is_(None)).order_by(User.id.desc())
            result = await db.execute(stmt)
            users = result.scalars().all()
            return [UserResponse.model_validate(u).model_dump() for u in users]

        async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
            async with async_session_factory() as db:
                try:
                    user_data = UserCreate(**data)
                    user = await create_user(db, user_data)
                    await db.commit()
                    return UserResponse.model_validate(user).model_dump()
                except Exception:
                    await db.rollback()
                    raise

        async def update_object(self, id: int, data: dict[str, Any]) -> dict[str, Any] | None:
            async with async_session_factory() as db:
                try:
                    stmt = select(User).where(User.id == id, User.deleted_at.is_(None))
                    result = await db.execute(stmt)
                    user = result.scalar_one_or_none()
                    if user is None:
                        return None

                    update_data = UserUpdateAdmin(**data).model_dump(exclude_unset=True)
                    password = update_data.pop("password", None)
                    if password:
                        update_data["password_hash"] = hash_password(password)

                    for field, value in update_data.items():
                        setattr(user, field, value)
                    await db.flush()
                    await db.refresh(user)
                    await db.commit()
                    return UserResponse.model_validate(user).model_dump()
                except Exception:
                    await db.rollback()
                    raise

        async def delete_object(self, id: int) -> bool:
            async with async_session_factory() as db:
                try:
                    from src.apps.core.base_repository import BaseRepository
                    from src.apps.users.models import User as UserModel

                    class UserRepo(BaseRepository):
                        model = UserModel

                    result = await UserRepo.soft_delete(db, id)
                    await db.commit()
                    return result is not None
                except Exception:
                    await db.rollback()
                    raise

        async def freeze_user(self, id: int) -> dict[str, Any] | None:
            return await self.update_object(id, {"status": "frozen"})

        async def unfreeze_user(self, id: int) -> dict[str, Any] | None:
            return await self.update_object(id, {"status": "active"})
