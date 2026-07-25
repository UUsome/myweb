from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.core.base_model import CoreModel


class Job(CoreModel):
    """Job listing - talent marketplace."""
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(200), nullable=False)
    company_logo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    salary_text: Mapped[str] = mapped_column(
        String(100), nullable=False,
        comment='e.g. "20K-35K·14薪"',
    )
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    industry: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    job_type: Mapped[str] = mapped_column(
        String(50), nullable=False, index=True,
        comment="全职/兼职/实习",
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    benefits: Mapped[list[str] | None] = mapped_column(
        JSON, nullable=True,
        comment='["五险一金", "年终奖"]',
    )
    tags: Mapped[list[dict] | None] = mapped_column(
        JSON, nullable=True,
        comment='[{"type": "internal", "label": "内推", "color": "#FF6B6B"}]',
    )
    contact_expert_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("experts.id", ondelete="SET NULL"),
        nullable=True, index=True,
    )
    contact_name: Mapped[str] = mapped_column(String(100), nullable=False)
    contact_id: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False,
        comment="Default contact expert ID (1)",
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationship
    contact_expert: Mapped["Expert | None"] = relationship(  # type: ignore[name-defined]
        "Expert", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, title={self.title}, company={self.company_name})>"
