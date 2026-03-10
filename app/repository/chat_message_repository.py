# app/infra/db/repository/chat_message_repository.py
from typing import List
from uuid import UUID

from sqlmodel import select, desc

from app.infra.db.db import DB
from app.models.chat.chat_message import ChatMessage
from app.schemas.message import Message


class MessageRepository:
    def __init__(self, db: DB):
        self.db = db

    async def add(self, session_id: UUID, role: str, content: str) -> ChatMessage:
        """新增消息，不立即 commit"""
        msg = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            position=0,  # position 先用 0，Service 层可以再计算
            extra={}
        )
        await self.db.flush(msg)  # flush 生成 id，但不 commit
        return msg

    async def get_last_position(self, session_id: UUID) -> int:
        """获取当前 session 最大 position"""
        stmt = (
            select(ChatMessage.position)
            .where(ChatMessage.session_id == session_id)
            .order_by(desc(ChatMessage.position))
            .limit(1)
        )
        result = await self.db.execute(stmt)
        last_position = result.scalar_one_or_none()
        return last_position or 0

    async def list_by_session(self, session_id: UUID, limit: int = 10) -> List[Message]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.position)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        db_messages = result.scalars().all()
        return [
            Message(role=m.role, content=m.content, meta=m.extra)
            for m in db_messages
        ]
