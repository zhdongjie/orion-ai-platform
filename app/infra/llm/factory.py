# app/infra/llm/factory.py

from app.core.config import settings
from app.infra.llm.base import BaseLLMProvider
from app.infra.llm.providers.openai_compatible import OpenAICompatibleProvider


def get_llm_client() -> BaseLLMProvider:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "qwen":
        return OpenAICompatibleProvider(
            api_key=settings.QWEN_API_KEY,
            base_url=settings.QWEN_API_BASE,
            chat_model=settings.QWEN_MODEL_LLM,
            embed_model=settings.QWEN_MODEL_EMBEDDING,
            timeout=settings.LLM_TIMEOUT
        )

    elif provider == "zhipu":
        return OpenAICompatibleProvider(
            api_key=settings.ZHIPU_API_KEY,
            base_url=settings.ZHIPU_API_BASE,
            chat_model=settings.ZHIPU_MODEL_GLM,
            embed_model=settings.ZHIPU_MODEL_EMBEDDING,
            timeout=settings.LLM_TIMEOUT
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")
