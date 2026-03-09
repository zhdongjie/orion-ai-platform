# app/schemas/chat.py
from typing import Optional, Dict, Any

from pydantic import Field

from app.schemas import BaseSchema


class ChatRequest(BaseSchema):
    query: str = Field(..., description="用户提问内容", examples=["你好，请介绍一下 Orion 平台"])
    history: Optional[list] = Field(default=[], description="历史对话记录")
    params: Optional[Dict[str, Any]] = Field(default={}, description="动态控制参数，如 temperature")


class ChatResponse(BaseSchema):
    answer: str = Field(..., description="模型返回的回答")
    usage: Optional[dict] = Field(default=None, description="Token 消耗统计")
