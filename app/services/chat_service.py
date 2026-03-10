# app/services/chat_service.py
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from loguru import logger
from sqlmodel import select, desc

from app.core.exceptions import PromptException, LLMProviderException
from app.infra.db.pgsql import async_session_maker
from app.infra.llm import llm_client
from app.models.chat.chat_message import ChatMessage
from app.models.chat.chat_session import ChatSession
from app.prompts import prompt_manager
from app.schemas import Result
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.message import Message


async def _get_or_create_session_id(session_id: Optional[UUID]) -> UUID:
    """确保会话存在"""
    async with async_session_maker() as db:
        if session_id:
            # 检查会话是否存在
            statement = select(ChatSession).where(ChatSession.id == session_id)
            result = await db.execute(statement)
            if result.scalar_one_or_none():
                return session_id

        # 创建新会话
        new_session = ChatSession(user_id="default_user", title="新对话")
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        return new_session.id


async def _load_history_from_db(session_id: UUID, limit: int) -> List[Message]:
    """从数据库读取历史并转为 Message Schema"""
    async with async_session_maker() as db:
        statement = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(desc(ChatMessage.created_at))
            .limit(limit)
        )
        result = await db.execute(statement)
        db_messages = result.scalars().all()

        # 按时间正序返回
        return [
            Message(role=m.role, content=m.content, meta=m.meta_data)
            for m in reversed(db_messages)
        ]


async def _save_message_to_db(session_id: UUID, role: str, content: str):
    """保存单条消息到数据库"""
    async with async_session_maker() as db:
        message_record = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
            meta_data={}
        )
        db.add(message_record)

        # 更新会话活跃时间
        statement = select(ChatSession).where(ChatSession.id == session_id)
        session_result = await db.execute(statement)
        session = session_result.scalar_one_or_none()
        if session:
            session.updated_at = datetime.now()
            db.add(session)

        await db.commit()


class ChatService:
    def __init__(self):
        self.client = llm_client

    async def chat(self, request: ChatRequest, prompt_path: str = "chat/general.yaml") -> Result[ChatResponse]:
        """
        集成了持久化和历史记录加载的对话服务
        """
        logger.info(f"开始处理对话请求: {request.query[:20]}...")

        # 1. 获取或创建会话 ID
        session_id = await _get_or_create_session_id(request.session_id)

        # 2. 加载历史消息 (从数据库加载最近 10 条)
        history_messages = await _load_history_from_db(session_id, limit=10)

        # 3. 准备提示词环境
        try:
            prompt_data = prompt_manager.load_prompt(prompt_path)
        except FileNotFoundError:
            raise PromptException(f"找不到提示词配置文件: {prompt_path}")

        system_content = prompt_data["messages"]["system"].format(
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # 4. 组装上下文 (将历史记录转为字符串，注入到模型调用中)
        # 注意：在 Phase 4 Agent 阶段，我们会直接传递 Message 列表给模型
        history_context = "\n".join([f"{m.role}: {m.content}" for m in history_messages])
        full_query = f"历史对话：\n{history_context}\n\n当前用户问题：{request.query}" if history_context else request.query

        try:
            # 5. 调用底层 LLM
            answer_content = await self.client.async_chat(
                query=full_query,
                system_prompt=system_content
            )

            # 6. 持久化：保存用户消息和 AI 消息
            await _save_message_to_db(session_id, "user", request.query)
            await _save_message_to_db(session_id, "assistant", answer_content)

            # 7. 组装返回对象
            response_message = Message(role="assistant", content=answer_content)

            logger.info(f"会话 {session_id} 响应成功")
            return Result.success(
                ChatResponse(
                    session_id=session_id,
                    message=response_message,
                    usage=None  # 后续对接 Provider 的 Token 统计
                )
            )

        except Exception as e:
            logger.exception(f"ChatService 异常: {str(e)}")
            raise LLMProviderException(f"模型调用或处理失败: {str(e)}")


# 实例化单例
chat_service = ChatService()
