from __future__ import annotations

import math
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class CursorPage(BaseModel, Generic[T]):
    """Cursor-based pagination for infinite scroll."""

    list: list[T]
    cursor: str | None = Field(
        None, description="Cursor for the next page (null if last page)"
    )
    has_next: bool = False


class OffsetPage(BaseModel, Generic[T]):
    """Offset-based pagination for admin backend."""

    list: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool = False
    total_pages: int = 0


def paginate_offset(
    items: list[T],
    total: int,
    page: int,
    page_size: int,
) -> OffsetPage[T]:
    """Create an offset-based pagination response."""
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0
    return OffsetPage(
        list=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=page < total_pages,
        total_pages=total_pages,
    )


def paginate_cursor(
    items: list[T],
    cursor_field: str = "id",
    limit: int = 20,
) -> CursorPage[T]:
    """Create a cursor-based pagination response.

    The cursor is the value of `cursor_field` on the last item.
    """
    has_next = len(items) > limit
    if has_next:
        items = items[:limit]

    cursor: str | None = None
    if items and has_next:
        last_item = items[-1]
        cursor = str(getattr(last_item, cursor_field))

    return CursorPage(
        list=items,
        cursor=cursor,
        has_next=has_next,
    )
