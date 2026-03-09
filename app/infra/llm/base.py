# app/infra/llm/base.py
from abc import ABC, abstractmethod
from typing import List


class BaseLLMProvider(ABC):
    """
    LLM 提供商的抽象基类 (相当于 Java 的 Interface)
    任何接入 Orion 平台的模型，都必须实现这两个方法。
    """

    @abstractmethod
    async def async_chat(self, query: str) -> str:
        """对话接口"""
        pass

    @abstractmethod
    async def async_embed(self, text: str) -> List[float]:
        """向量化接口"""
        pass
