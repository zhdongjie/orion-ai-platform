# app/infra/llm/providers/openai_compatible.py

from typing import List

from langchain_core.messages import BaseMessage, AIMessage
from openai import AsyncOpenAI

from app.infra.llm.base import BaseLLMProvider
from app.infra.llm.message_adapter import lc_to_openai


class OpenAICompatibleProvider(BaseLLMProvider):
    """
    万能的 OpenAI 兼容协议实现类
    只要厂商支持 OpenAI 接口规范，统统可以用这个类实例化
    """

    def __init__(self, api_key: str, base_url: str, chat_model: str, embed_model: str, timeout: int):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout
        )
        self.chat_model = chat_model
        self.embed_model = embed_model

    async def async_chat(self, messages: List[BaseMessage]) -> AIMessage:
        """
        LangChain Message → OpenAI API → AIMessage
        """

        # LangChain message 转 OpenAI message
        openai_messages = lc_to_openai(messages)

        response = await self.client.chat.completions.create(
            model=self.chat_model,
            messages=openai_messages,
            temperature=0.7
        )

        content = response.choices[0].message.content

        return AIMessage(content=content)

    async def async_embed(self, text: str) -> List[float]:
        """
        文本向量化
        """

        response = await self.client.embeddings.create(
            model=self.embed_model,
            input=text
        )

        return response.data[0].embedding
