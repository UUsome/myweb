from __future__ import annotations

import time
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")
DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[T]):
    """Unified API response format."""

    code: int = 0
    message: str = "success"
    data: T | None = None
    timestamp: int = Field(default_factory=lambda: int(time.time()))


class PageResponse(BaseModel, Generic[DataT]):
    """Offset pagination response data wrapper."""

    list: list[DataT]
    total: int
    page: int
    page_size: int
    has_next: bool


def success(data: T | None = None, message: str = "success") -> APIResponse[T]:
    """Create a success response."""
    return APIResponse(code=0, message=message, data=data)


def error(code: int, message: str, data: T | None = None) -> APIResponse[T]:
    """Create an error response."""
    return APIResponse(code=code, message=message, data=data)
