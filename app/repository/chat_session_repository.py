# app/infra/db/repository/chat_session_repository.py
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from app.infra.db.crud import DB
from app.models.chat.chat_session import ChatSession


class SessionRepository:
    def __init__(self, db: DB):
        self.db = db

    async def get_or_create(self, session_id: Optional[UUID]) -> ChatSession:
        if session_id:
            session = await self.db.get(ChatSession, session_id)
            if session:
                return session

        # 新建 session
        new_session = ChatSession(user_id="default_user", title="新对话")
        await self.db.add(new_session)
        await self.db.flush()  # 生成 ID
        return new_session

    async def update_timestamp(self, session_id: UUID):
        session = await self.db.get(ChatSession, session_id)
        if session:
            session.updated_at = datetime.now(timezone.utc)
            await self.db.add(session)
