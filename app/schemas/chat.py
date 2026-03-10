# app/schemas/chat.py
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import Field

from app.schemas import BaseSchema
from app.schemas.message import Message
from app.schemas.usage import Usage


class ChatRequest(BaseSchema):
    """
    聊天请求
    """

    session_id: Optional[UUID] = Field(
        default=None,
        description="会话ID，不传则创建新会话"
    )

    query: str = Field(
        ...,
        description="用户输入问题",
        examples=["你好，请介绍一下 Orion 平台"]
    )

    history: List[Message] = Field(
        default_factory=list,
        description="历史对话（可选，通常由后端加载）"
    )

    params: Dict[str, Any] = Field(
        default_factory=dict,
        description="模型参数，如 temperature、top_p"
    )


class ChatResponse(BaseSchema):
    """
    聊天返回
    """

    session_id: UUID = Field(
        ...,
        description="会话ID"
    )

    message: Message = Field(
        ...,
        description="AI返回消息"
    )

    usage: Optional[Usage] = Field(
        default=None,
        description="Token统计"
    )