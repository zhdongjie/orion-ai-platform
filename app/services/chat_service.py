# app/services/chat_service.py
from datetime import datetime

from loguru import logger

from app.core.exceptions import PromptException, LLMProviderException
from app.infra.llm import llm_client
from app.prompts import prompt_manager
from app.schemas import Result
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self):
        self.client = llm_client

    async def chat(self, request: ChatRequest, prompt_path: str = "chat/general.yaml") -> Result[ChatResponse]:
        """
        通用的对话服务逻辑
        """
        logger.info(f"开始处理对话请求: {request.query[:20]}...")
        # 1. 加载提示词配置
        try:
            prompt_data = prompt_manager.load_prompt(prompt_path)
        except FileNotFoundError:
            raise PromptException(f"找不到提示词配置文件: {prompt_path}")
        # 2. 准备系统提示词 (注入动态变量，如当前时间)
        system_content = prompt_data["messages"]["system"].format(
            current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        try:
            # 3. 调用底层 Provider
            answer = await self.client.async_chat(
                query=request.query,
                system_prompt=system_content
            )

            logger.info("模型响应成功")
            return Result.success(ChatResponse(answer=answer))

        except Exception as e:
            logger.error(f"ChatService 异常: {str(e)}")
            raise LLMProviderException(f"底层模型调用失败: {str(e)}")


# 实例化单例
chat_service = ChatService()
