# app/services/chat_service.py
from datetime import datetime, timezone

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger

from app.core.constants import ResponseCode, MessageRole
from app.core.exceptions import PromptException, LLMProviderException, BusinessException
from app.infra.db.db import get_db
from app.infra.llm import llm_client
from app.infra.llm.message_adapter import schema_to_lc
from app.prompts import prompt_manager
from app.repository.chat_message_repository import MessageRepository
from app.repository.chat_session_repository import SessionRepository
from app.schemas import Result
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.message import Message


class ChatService:
    def __init__(self):
        self.client = llm_client

    async def chat(self, request: ChatRequest, prompt_path: str = "chat/general.yaml") -> Result[ChatResponse]:
        logger.info(f"开始处理对话请求: {request.query[:20]}...")

        if not request.query:
            raise BusinessException("聊天内容不能为空", code=ResponseCode.SYSTEM_ERROR)

        async with get_db() as db:  # DB 封装，单个事务
            session_repo = SessionRepository(db)
            msg_repo = MessageRepository(db)

            # 1. 获取或创建 session
            session = await session_repo.get_or_create(request.session_id)

            session_id = session.id

            # 2. 加载历史消息
            history_messages = await msg_repo.list_by_session(session_id, limit=10)

            # 3. 加载 Prompt
            try:
                prompt_data = prompt_manager.load_prompt(prompt_path)
            except FileNotFoundError:
                raise PromptException(f"找不到提示词配置文件: {prompt_path}")

            system_content = prompt_data["messages"]["system"].format(
                current_time=datetime.now(timezone.utc).isoformat()
            )

            # 4. 构建 LangChain Messages
            messages = [SystemMessage(content=system_content)]
            messages.extend(schema_to_lc(history_messages))
            messages.append(HumanMessage(content=request.query))

            try:
                # 5. 保存用户消息
                last_pos = await msg_repo.get_last_position(session_id)
                human_msg = await msg_repo.add(session_id, role=MessageRole.USER, content=request.query)
                human_msg.position = last_pos + 1

                # 6. 调用 LLM
                ai_message = await self.client.async_chat(messages)
                answer_content = ai_message.content

                # 7. 保存 AI 回复
                last_pos = human_msg.position
                ai_msg = await msg_repo.add(session_id, role=MessageRole.ASSISTANT, content=answer_content)
                ai_msg.position = last_pos + 1

                # 8. 更新 session 更新时间
                session.updated_at = datetime.now(timezone.utc)

                # 9. 最后统一 commit
                await db.update()  # 这里会 commit 所有 flush 的对象

                # 10. 返回响应
                response_message = Message(role=MessageRole.ASSISTANT, content=answer_content)
                logger.info(f"会话 {session_id} 响应成功")

                return Result.success(
                    ChatResponse(session_id=session_id, message=response_message, usage=None)
                )

            except Exception as e:
                logger.error(f"ChatService 异常: {str(e)}")
                raise LLMProviderException(f"模型调用失败: {str(e)}")


chat_service = ChatService()
