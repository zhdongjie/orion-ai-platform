# app/models/chat/chat_message.py
from typing import Dict, Any, TYPE_CHECKING
from uuid import UUID

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, Relationship, Column

from app.models.base import BaseModel
from app.models.mixins import (
    TimestampMixin,
    TenantMixin,
    SoftDeleteMixin
)

if TYPE_CHECKING:
    from app.models.chat.chat_session import ChatSession


class ChatMessage(
    BaseModel,
    TimestampMixin,
    TenantMixin,
    SoftDeleteMixin,
    table=True
):
    __tablename__ = "chat_messages"

    session_id: UUID = Field(foreign_key="chat_sessions.id", index=True)
    role: str = Field(max_length=20)  # system, user, assistant, tool
    position: int = Field(index=True)
    content: str

    # 使用 JSONB 存储元数据（Token 消耗、引用源等）
    extra: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))

    # 关联会话
    session: "ChatSession" = Relationship(back_populates="messages")
