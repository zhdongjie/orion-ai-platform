# app/schemas/message.py
from typing import Literal, Optional, Dict, Any

from pydantic import Field

from app.schemas import BaseSchema


class Message(BaseSchema):
    """
    标准对话消息结构
    """

    role: Literal["system", "user", "assistant", "tool"] = Field(
        ...,
        description="消息角色"
    )

    content: str = Field(
        ...,
        description="消息内容"
    )

    meta: Optional[Dict[str, Any]] = Field(
        default=None,
        description="扩展信息（tool、引用来源等）"
    )
