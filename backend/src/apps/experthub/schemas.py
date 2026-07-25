from __future__ import annotations

from pydantic import Field

from src.apps.core.base_schema import CoreSchema, TimestampSchema


# ── Tag / Service Definitions ──


class TagDefinitionBase(CoreSchema):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: str | None = None
    sort_order: int = 0


class TagDefinitionResponse(TimestampSchema):
    id: int
    name: str
    slug: str
    description: str | None = None
    sort_order: int = 0


class ServiceDefinitionBase(CoreSchema):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: str | None = None
    sort_order: int = 0


class ServiceDefinitionResponse(TimestampSchema):
    id: int
    name: str
    slug: str
    description: str | None = None
    sort_order: int = 0


# ── Platform ──


class PlatformBase(CoreSchema):
    platform_type: str = Field(..., max_length=50)
    platform_name: str = Field(..., max_length=100)
    icon: str | None = None
    blogger_name: str = Field(..., max_length=100)
    profile: str | None = None
    url: str | None = None
    sort_order: int = 0


class PlatformResponse(TimestampSchema):
    id: int
    expert_id: int
    platform_type: str
    platform_name: str
    icon: str | None = None
    blogger_name: str
    profile: str | None = None
    url: str | None = None
    sort_order: int = 0


# ── Case ──


class CaseBase(CoreSchema):
    name: str = Field(..., max_length=200)
    summary: str | None = None
    content: str | None = None
    cover_image: str | None = None
    sort_order: int = 0


class CaseResponse(TimestampSchema):
    id: int
    expert_id: int
    name: str
    summary: str | None = None
    content: str | None = None
    cover_image: str | None = None
    sort_order: int = 0


# ── Expert ──


class ExpertBase(CoreSchema):
    name: str = Field(..., max_length=100)
    title: str | None = None
    summary: str = Field(...)
    avatar_url: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    contact_wechat: str | None = None
    is_published: bool = True
    sort_order: int = 0


class ExpertCreate(ExpertBase):
    tag_ids: list[int] = []
    service_ids: list[int] = []


class ExpertUpdate(CoreSchema):
    name: str | None = None
    title: str | None = None
    summary: str | None = None
    avatar_url: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    contact_wechat: str | None = None
    is_published: bool | None = None
    sort_order: int | None = None
    tag_ids: list[int] | None = None
    service_ids: list[int] | None = None


class ExpertListResponse(TimestampSchema):
    id: int
    name: str
    title: str | None = None
    summary: str
    avatar_url: str | None = None
    platform_count: int = 0
    case_count: int = 0
    is_published: bool = True
    sort_order: int = 0
    tags: list[TagDefinitionResponse] = []
    services: list[ServiceDefinitionResponse] = []


class ExpertDetailResponse(ExpertListResponse):
    contact_email: str | None = None
    contact_phone: str | None = None
    contact_wechat: str | None = None
    platforms: list[PlatformResponse] = []
    cases: list[CaseResponse] = []


class ExpertHoverResponse(CoreSchema):
    """Hover card data for expert."""
    id: int
    name: str
    title: str | None = None
    summary: str
    avatar_url: str | None = None
    platform_count: int = 0
    case_count: int = 0
    platforms: list[PlatformResponse] = []
    cases: list[CaseResponse] = []
    tags: list[TagDefinitionResponse] = []


class ContactContent(CoreSchema):
    content: str = Field(default="", description="Markdown 内容")
