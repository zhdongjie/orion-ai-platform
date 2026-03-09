# app/infra/llm/__init__.py
from app.core.config import settings
from app.infra.llm.base import BaseLLMProvider


def get_llm_client() -> BaseLLMProvider:
    """
    大模型工厂：根据环境变量动态返回对应的 LLM 客户端实例
    """
    provider = settings.LLM_PROVIDER.lower()

    if provider == "qwen":
        from app.infra.llm.qwen_provider import QwenProvider
        return QwenProvider()
    elif provider == "zhipu":
        from app.infra.llm.zhipu_provider import ZhipuProvider
        return ZhipuProvider()
    else:
        raise ValueError(f"不支持的 LLM 提供商: {provider}")


# 实例化全局单例客户端供上层调用
llm_client = get_llm_client()
