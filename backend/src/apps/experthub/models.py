from __future__ import annotations

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.core.base_model import CoreModel

# ── Many-to-Many association tables ──

expert_tags = Table(
    "expert_tags",
    CoreModel.metadata,
    Column("expert_id", Integer, ForeignKey("experts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("expert_tag_definitions.id"), primary_key=True),
)

expert_services = Table(
    "expert_services",
    CoreModel.metadata,
    Column("expert_id", Integer, ForeignKey("experts.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("expert_service_definitions.id"), primary_key=True),
)


# ── Tag / Service Definitions ──


class TagDefinition(CoreModel):
    """Expert tag/category definition."""
    __tablename__ = "expert_tag_definitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class ServiceDefinition(CoreModel):
    """Expert service type definition."""
    __tablename__ = "expert_service_definitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Expert(CoreModel):
    """Expert card - main model."""
    __tablename__ = "experts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    title: Mapped[str | None] = mapped_column(String(200), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    contact_wechat: Mapped[str | None] = mapped_column(String(100), nullable=True)
    platform_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    case_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    tags: Mapped[list["TagDefinition"]] = relationship(
        "TagDefinition", secondary=expert_tags, lazy="selectin"
    )
    services: Mapped[list["ServiceDefinition"]] = relationship(
        "ServiceDefinition", secondary=expert_services, lazy="selectin"
    )
    platforms: Mapped[list["Platform"]] = relationship(
        "Platform", back_populates="expert", lazy="selectin",
        order_by="Platform.sort_order",
    )
    cases: Mapped[list["Case"]] = relationship(
        "Case", back_populates="expert", lazy="selectin",
        order_by="Case.sort_order",
    )

    def __repr__(self) -> str:
        return f"<Expert(id={self.id}, name={self.name})>"


class Platform(CoreModel):
    """Expert platform account (one-to-many with Expert)."""
    __tablename__ = "expert_platforms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    expert_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("experts.id"), nullable=False, index=True
    )
    platform_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # douyin / xiaohongshu / wechat_video
    platform_name: Mapped[str] = mapped_column(String(100), nullable=False)
    icon: Mapped[str | None] = mapped_column(String(500), nullable=True)
    blogger_name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    expert: Mapped[Expert] = relationship("Expert", back_populates="platforms")

    def __repr__(self) -> str:
        return f"<Platform(id={self.id}, type={self.platform_type}, blogger={self.blogger_name})>"


class Case(CoreModel):
    """Expert case/portfolio (one-to-many with Expert)."""
    __tablename__ = "expert_cases"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    expert_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("experts.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)  # Markdown
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    expert: Mapped[Expert] = relationship("Expert", back_populates="cases")

    def __repr__(self) -> str:
        return f"<Case(id={self.id}, name={self.name})>"
