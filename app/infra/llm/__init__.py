# app/infra/llm/__init__.py
from typing import List

from openai import AsyncOpenAI

from app.core.config import settings
from app.infra.llm.base import BaseLLMProvider


def get_llm_client() -> BaseLLMProvider:
    """
    大模型工厂：根据环境变量动态返回对应的 LLM 客户端实例
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "qwen":
        return OpenAICompatibleProvider(
            api_key=settings.QWEN_API_KEY,
            base_url=settings.QWEN_API_BASE,
            chat_model=settings.QWEN_MODEL_LLM,
            embed_model=settings.QWEN_MODEL_EMBEDDING
        )
    elif provider == "zhipu":
        return OpenAICompatibleProvider(
            api_key=settings.ZHIPU_API_KEY,
            base_url=settings.ZHIPU_API_BASE,
            chat_model=settings.ZHIPU_MODEL_GLM,
            embed_model=settings.ZHIPU_MODEL_EMBEDDING
        )
    else:
        raise ValueError(f"不支持的 LLM 提供商: {provider}")


class OpenAICompatibleProvider(BaseLLMProvider):
    """
    万能的 OpenAI 兼容协议实现类
    只要厂商支持 OpenAI 接口规范，统统可以用这个类实例化！
    """

    def __init__(self, api_key: str, base_url: str, chat_model: str, embed_model: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.chat_model = chat_model
        self.embed_model = embed_model

    async def async_chat(self, query: str, system_prompt: str = None) -> str:
        # 💡 构建消息列表
        messages = []

        # 如果传入了系统提示词，把它放在最前面
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            # 也可以在这里设置一个极其简单的默认兜底
            messages.append({"role": "system", "content": "你是一个有帮助的助手。"})

        # 放入用户的问题
        messages.append({"role": "user", "content": query})
        response = await self.client.chat.completions.create(
            model=self.chat_model,
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content

    async def async_embed(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            model=self.embed_model,
            input=text
        )
        return response.data[0].embedding


# 实例化全局单例客户端供上层调用
llm_client = get_llm_client()
