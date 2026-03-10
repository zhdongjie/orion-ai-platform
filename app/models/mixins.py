# app/models/mixins.py
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel, table=False):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )


class SoftDeleteMixin(SQLModel):
    """
    软删除
    """

    is_deleted: bool = Field(default=False, index=True)


class TenantMixin(SQLModel):
    """
    多租户
    """

    tenant_id: str = Field(index=True, default_factory=lambda: str(uuid.uuid4()))


class AuditMixin(SQLModel):
    """
    审计字段
    """

    created_by: Optional[str] = Field(default=None, index=True)
    updated_by: Optional[str] = Field(default=None, index=True)
