from __future__ import annotations

from typing import Annotated

from fastapi import Query


async def pagination_params(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
) -> tuple[int, int]:
    """Offset pagination dependency."""
    return page, page_size


async def cursor_pagination_params(
    cursor: Annotated[str | None, Query(description="Cursor for next page")] = None,
    limit: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 20,
) -> tuple[str | None, int]:
    """Cursor pagination dependency."""
    return cursor, limit


async def sort_params(
    sort_by: Annotated[str | None, Query(description="Sort field")] = None,
    sort_order: Annotated[
        str, Query(pattern="^(asc|desc)$", description="Sort direction")
    ] = "desc",
) -> tuple[str | None, str]:
    """Sort parameters dependency."""
    return sort_by, sort_order
