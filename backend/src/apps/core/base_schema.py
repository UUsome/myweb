from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class CoreSchema(BaseModel):
    """Base schema with common configuration."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        },
    )


class TimestampSchema(CoreSchema):
    """Schema with timestamp fields."""

    created_at: datetime | None = None
    updated_at: datetime | None = None
