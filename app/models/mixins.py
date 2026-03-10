# app/models/mixin.py
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime
from sqlmodel import Field


def utc_now():
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: datetime = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),  # type: ignore
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=utc_now,
        sa_type=DateTime(timezone=True),  # type: ignore
        nullable=False
    )


class SoftDeleteMixin:
    is_deleted: bool = Field(default=False, index=True)


class TenantMixin:
    tenant_id: str = Field(
        index=True,
        default_factory=lambda: str(uuid.uuid4())
    )


class AuditMixin:
    created_by: Optional[str] = Field(default=None, index=True)
    updated_by: Optional[str] = Field(default=None, index=True)
