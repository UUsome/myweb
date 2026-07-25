from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.apps.core.response import PageResponse, success
from src.apps.users.dependencies import get_current_admin_user
from src.apps.users.models import User
from src.core.database import async_session_factory

router = APIRouter(prefix="/admin", tags=["Admin"])


class ModelAdmin:
    """Base class for model admin configuration."""

    list_display: list[str] = ["id"]
    list_filter: dict[str, list[Any]] = {}
    search_fields: list[str] = []
    list_per_page: int = 20
    model_schema_create: type | None = None
    model_schema_update: type | None = None
    model_schema_response: type | None = None

    async def get_queryset(self, db: AsyncSession) -> list[dict[str, Any]]:
        raise NotImplementedError

    async def create_object(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    async def update_object(self, id: int, data: dict[str, Any]) -> dict[str, Any] | None:
        raise NotImplementedError

    async def delete_object(self, id: int) -> bool:
        raise NotImplementedError

    def get_list_display(self) -> list[str]:
        return self.list_display


class AdminSite:
    """Lightweight admin site for managing app models."""

    def __init__(self) -> None:
        self._registry: dict[str, type[ModelAdmin]] = {}
        self._router = APIRouter(prefix="/admin", tags=["Admin API"])

    def register(
        self, model_class: type, admin_class: type[ModelAdmin] | None = None
    ) -> Callable[[type[ModelAdmin]], type[ModelAdmin]] | None:
        """Register a model with an optional admin class.

        Can be used as a decorator:
            @site.register(Model)
            class ModelAdmin(ModelAdmin): ...
        """
        model_name = model_class.__tablename__ if hasattr(model_class, "__tablename__") else model_class.__name__.lower()

        if admin_class is not None:
            instance = admin_class()
            self._registry[model_name] = instance
            self._register_routes(model_name, instance)
            return None

        def wrapper(admin_cls: type[ModelAdmin]) -> type[ModelAdmin]:
            instance = admin_cls()
            self._registry[model_name] = instance
            self._register_routes(model_name, instance)
            return admin_cls

        return wrapper

    def _register_routes(self, model_name: str, admin: ModelAdmin) -> None:
        """Register CRUD routes for a model."""

        @self._router.get(
            f"/{model_name}",
            summary=f"{model_name}列表",
            description=f"Admin: 获取{model_name}列表",
        )
        async def admin_list(
            page: int = 1,
            page_size: int = 20,
            admin_user: User = Depends(get_current_admin_user),
        ) -> Any:
            async with async_session_factory() as db:
                items = await admin.get_queryset(db)

            total = len(items)
            start = (page - 1) * page_size
            end = start + page_size
            page_items = items[start:end]

            return success(
                data=PageResponse(
                    list=page_items,
                    total=total,
                    page=page,
                    page_size=page_size,
                    has_next=end < total,
                )
            )

        @self._router.post(
            f"/{model_name}",
            summary=f"创建{model_name}",
            description=f"Admin: 创建新的{model_name}",
        )
        async def admin_create(
            data: dict[str, Any],
            admin_user: User = Depends(get_current_admin_user),
        ) -> Any:
            result = await admin.create_object(data)
            return success(data=result, message=f"{model_name}创建成功")

        @self._router.put(
            f"/{model_name}/{{item_id}}",
            summary=f"更新{model_name}",
            description=f"Admin: 更新{model_name}信息",
        )
        async def admin_update(
            item_id: int,
            data: dict[str, Any],
            admin_user: User = Depends(get_current_admin_user),
        ) -> Any:
            result = await admin.update_object(item_id, data)
            if result is None:
                from src.apps.core.exceptions import NotFound
                raise NotFound(message=f"{model_name}不存")
            return success(data=result, message=f"{model_name}更新成功")

        @self._router.delete(
            f"/{model_name}/{{item_id}}",
            summary=f"删除{model_name}",
            description=f"Admin: 删除{model_name}",
        )
        async def admin_delete(
            item_id: int,
            admin_user: User = Depends(get_current_admin_user),
        ) -> Any:
            deleted = await admin.delete_object(item_id)
            if not deleted:
                from src.apps.core.exceptions import NotFound
                raise NotFound(message=f"{model_name}不存在")
            return success(message=f"{model_name}删除成功")

    @property
    def router(self) -> APIRouter:
        return self._router

    def get_registered_models(self) -> dict[str, type[ModelAdmin]]:
        return self._registry
