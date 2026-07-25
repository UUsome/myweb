from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import Field

from src.apps.core.base_schema import CoreSchema, TimestampSchema


class JobTagSchema(CoreSchema):
    type: str = Field(..., description="internal/urgent/expert")
    label: str
    color: str = "#666666"


class JobBase(CoreSchema):
    title: str = Field(..., max_length=200)
    company_name: str = Field(..., max_length=200)
    company_logo: str | None = None
    salary_text: str = Field(..., max_length=100)
    city: str = Field(..., max_length=100)
    industry: str = Field(..., max_length=100)
    job_type: str = Field(..., max_length=50)
    description: str | None = None
    requirements: str | None = None
    benefits: list[str] | None = None
    tags: list[JobTagSchema] | None = None
    contact_expert_id: int | None = None
    contact_name: str = Field(..., max_length=100)
    is_active: bool = True
    is_featured: bool = False
    expires_at: datetime | None = None


class JobCreate(JobBase):
    pass


class JobUpdate(CoreSchema):
    title: str | None = None
    company_name: str | None = None
    company_logo: str | None = None
    salary_text: str | None = None
    city: str | None = None
    industry: str | None = None
    job_type: str | None = None
    description: str | None = None
    requirements: str | None = None
    benefits: list[str] | None = None
    tags: list[JobTagSchema] | None = None
    contact_expert_id: int | None = None
    contact_name: str | None = None
    is_active: bool | None = None
    is_featured: bool | None = None
    expires_at: datetime | None = None


class JobListResponse(TimestampSchema):
    id: int
    title: str
    company_name: str
    company_logo: str | None = None
    salary_text: str
    city: str
    industry: str
    job_type: str
    tags: list[JobTagSchema] = []
    is_active: bool = True
    is_featured: bool = False
    view_count: int = 0
    contact_name: str = ""
    contact_expert_id: int | None = None


class JobDetailResponse(JobListResponse):
    description: str | None = None
    requirements: str | None = None
    benefits: list[str] | None = None
    expires_at: datetime | None = None
    contact_expert: dict[str, Any] | None = None  # Expert brief info


class JobFilterOptions(CoreSchema):
    cities: list[str] = []
    industries: list[str] = []
    job_types: list[str] = []


class JobTagAvailable(CoreSchema):
    type: str
    label: str
    color: str
    description: str = ""
