# app/models/chat/chat_session.py
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel
from app.models.mixins import (
    TimestampMixin,
    TenantMixin,
    SoftDeleteMixin
)

if TYPE_CHECKING:
    from app.models.chat.chat_message import ChatMessage


class ChatSession(
    BaseModel,
    TimestampMixin,
    TenantMixin,
    SoftDeleteMixin,
    table=True
):
    __tablename__ = "chat_sessions"

    user_id: str = Field(index=True)
    title: Optional[str] = Field(default="新对话")

    # 关联消息
    messages: List["ChatMessage"] = Relationship(back_populates="session")
